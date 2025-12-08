from fastapi import APIRouter, Depends, HTTPException, Header, status
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
        from fastapi.responses import Response
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
    return game


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
    return game


# Endpoint to make a guess in an existing game
@router.post("/{game_id}/guess", response_model=schemas.GameRead)
def guess(game_id: int, payload: schemas.GuessIn, session: Session = Depends(get_session)):
    game = session.get(models.Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    word = session.get(models.Word, game.word_id)
    letter = payload.letter.lower()
    if letter in word.text.lower():
        # reveal occurrences
        new = list(game.revealed)
        for i, ch in enumerate(word.text.lower()):
            if ch == letter:
                new[i] = word.text[i]
        game.revealed = "".join(new)
        # simple scoring
        game.score += word.text.lower().count(letter) * 10
    else:
        game.attempts_left -= 1
        if game.attempts_left <= 0:
            game.state = "lost"
    # check win
    if "_" not in game.revealed:
        game.state = "won"
    session.add(game)
    session.commit()
    session.refresh(game)
    return game
