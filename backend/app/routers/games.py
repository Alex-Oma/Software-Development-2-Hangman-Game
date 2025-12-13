from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.responses import Response
from sqlmodel import Session, select
from sqlalchemy import desc
from typing import Optional
from .. import schemas, crud, models
from ..deps import get_session
from ..core import security
from jose import jwt

# Router for game-related endpoints
router = APIRouter()


# helper dependency to get current user from Authorization header (Bearer token)
def get_current_user(authorization: Optional[str] = Header(None), session: Session = Depends(get_session)) -> models.User:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        scheme, token = authorization.split()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth header")
    if scheme.lower() != 'bearer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unsupported auth scheme")
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        sub = payload.get('sub')
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user_id = int(sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def try_get_user_from_header(authorization: Optional[str], session: Session) -> Optional[models.User]:
    """Try to resolve a user from Authorization header, return None if missing/invalid."""
    if not authorization:
        return None
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            return None
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        sub = payload.get('sub')
        if not sub:
            return None
        user_id = int(sub)
        return session.get(models.User, user_id)
    except Exception:
        return None


# Endpoint to check for an unfinished (active) game for the current user
@router.get("/unfinished", response_model=Optional[schemas.GameRead], status_code=200)
def get_unfinished_game(current_user: models.User = Depends(get_current_user), session: Session = Depends(get_session)):
    # find the most recent game for this user with state == 'active'
    stmt = select(models.Game).where(models.Game.user_id == current_user.id, models.Game.state == 'active').order_by(desc(models.Game.created_at)).limit(1)
    game = session.exec(stmt).first()
    if not game:
        # No unfinished game - return 204 No Content
        return Response(status_code=204)
    return game


# Endpoint to start a new game
@router.post("/new", response_model=schemas.GameRead)
def new_game(payload: schemas.GameCreate, session: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    """Create a new game for the authenticated user. Requires a valid Bearer token."""
    word = crud.get_random_word(session, payload.topic, payload.difficulty)
    if not word:
        raise HTTPException(status_code=404, detail="No words available")

    # current_user is provided by get_current_user and will raise 401 if auth is missing/invalid
    game = crud.create_game(session, current_user, word)
    # ensure the created game includes the selected word relationship so the response contains topic/clue
    try:
        game.word = word
        session.add(game)
        session.commit()
        session.refresh(game)
    except Exception:
        # best-effort: if refresh fails, return the game as-is
        session.rollback()

    # Build response payload that excludes the actual word text so that user can't cheat!
    word_meta = {
        'id': word.id,
        'clue': word.clue,
        'topic': word.topic,
        'difficulty': word.difficulty,
    }
    response = {
        'id': game.id,
        'revealed': game.revealed,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'word': word_meta,
    }
    return response


# Endpoint to get a game by id (used for resume)
@router.get("/{game_id}", response_model=schemas.GameRead)
def get_game(game_id: int, session: Session = Depends(get_session), authorization: Optional[str] = Header(None)):
    game = session.get(models.Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    # If an Authorization header is present, ensure the caller owns the game
    user = try_get_user_from_header(authorization, session)
    if user and game.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to access this game")

    # Build explicit response that contains only word metadata (no word.text) so that user can't cheat
    word_meta = None
    try:
        if getattr(game, 'word_id', None) is not None:
            w = session.get(models.Word, game.word_id)
            if w:
                word_meta = {
                    'id': w.id,
                    'clue': w.clue,
                    'topic': w.topic,
                    'difficulty': w.difficulty,
                }
    except Exception:
        # ignore failures to build metadata; return best-effort response below
        word_meta = None

    response = {
        'id': game.id,
        'revealed': game.revealed,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'word': word_meta,
    }
    return response


# Endpoint to make a guess in an existing game
@router.post("/{game_id}/guess", response_model=schemas.GameRead)
def guess(game_id: int, payload: schemas.GuessIn, session: Session = Depends(get_session)):
    game = session.get(models.Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Only allow guesses when the game is actively in progress otherwise return 409 Conflict
    if game.state != 'active':
        # Game already finished (won/lost) or otherwise inactive - inform the client
        raise HTTPException(status_code=409, detail=f"Game is not active (state={game.state}). Start a new game to continue.")

    # Validate the letter input
    word = session.get(models.Word, game.word_id)
    letter = payload.letter.lower()
    # normalize guessed storage
    guessed_set = set((game.guessed or '').lower()) if game.guessed is not None else set()
    if letter in guessed_set:
        # Letter has already been guessed; don't apply scoring or change attempts
        raise HTTPException(status_code=409, detail=f"Letter '{letter}' was already guessed")
    if letter in word.text.lower():
        # reveal occurrences
        new = list(game.revealed)
        for i, ch in enumerate(word.text.lower()):
            if ch == letter:
                new[i] = word.text[i]
        game.revealed = "".join(new)
        # simple scoring
        # increase score only for newly discovered occurrences
        game.score += word.text.lower().count(letter) * 10
        # record guessed letter
        guessed_set.add(letter)
        game.guessed = ''.join(sorted(guessed_set))
    else:
        game.attempts_left -= 1
        # record guessed letter even if incorrect
        guessed_set.add(letter)
        game.guessed = ''.join(sorted(guessed_set))
        if game.attempts_left <= 0:
            game.state = "lost"

    # check win condition
    if "_" not in game.revealed:
        game.state = "won"

    # save the game state
    session.add(game)
    session.commit()
    session.refresh(game)

    # Build explicit response that contains only word metadata (no word.text) so that user can't cheat
    word_meta = None
    try:
        if getattr(game, 'word_id', None) is not None:
            w = session.get(models.Word, game.word_id)
            if w:
                word_meta = {
                    'id': w.id,
                    'clue': w.clue,
                    'topic': w.topic,
                    'difficulty': w.difficulty,
                }
    except Exception:
        # ignore failures to build metadata; return best-effort response below
        word_meta = None

    # Build the response payload
    response = {
        'id': game.id,
        'revealed': game.revealed,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'word': word_meta,
    }
    # return the updated game state
    return response
