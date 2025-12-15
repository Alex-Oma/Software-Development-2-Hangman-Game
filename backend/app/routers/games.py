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
    # Resolve the current user from the Authorization header
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        # split "Bearer <token>"
        scheme, token = authorization.split()
    except Exception:
        # malformed header
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth header")
    if scheme.lower() != 'bearer':
        # unsupported auth scheme
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unsupported auth scheme")
    try:
        # decode the JWT token
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        # extract user id from 'sub' claim
        sub = payload.get('sub')
        # validate sub
        if not sub:
            # missing sub claim
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        # convert sub to int user id
        user_id = int(sub)
    except Exception:
        # token decoding/validation failed
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # fetch the user from the database
    user = session.get(models.User, user_id)
    # validate user exists
    if not user:
        # user not found
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # return the authenticated user back to the frontend
    return user


def try_get_user_from_header(authorization: Optional[str], session: Session) -> Optional[models.User]:
    """Try to resolve a user from Authorization header, return None if missing/invalid."""
    # If no Authorization header, return None
    if not authorization:
        return None
    try:
        # split "Bearer <token>"
        scheme, token = authorization.split()
        # validate scheme
        if scheme.lower() != 'bearer':
            # unsupported auth scheme
            return None
        # decode the JWT token
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        # extract user id from 'sub' claim
        sub = payload.get('sub')
        # validate sub
        if not sub:
            return None
        # convert sub to int user id
        user_id = int(sub)
        # fetch the user from the database
        return session.get(models.User, user_id)
    except Exception:
        # any failure returns None
        return None


# Endpoint to check for an unfinished (active) game for the current user
@router.get("/unfinished", response_model=Optional[schemas.GameRead], status_code=200)
def get_unfinished_game(current_user: models.User = Depends(get_current_user), session: Session = Depends(get_session)):
    # find the most recent game for this user with state == 'active'
    stmt = select(models.Game).where(models.Game.user_id == current_user.id, models.Game.state == 'active').order_by(desc(models.Game.created_at)).limit(1)
    # execute the query
    game = session.exec(stmt).first()
    # if no active game found, return 204 No Content
    if not game:
        # No unfinished game - return 204 No Content
        return Response(status_code=204)

    # Build explicit response that contains only word metadata (no word.text) so that user can't cheat
    word_meta = None
    # attempt to build word metadata
    try:
        # only attempt if word_id is present
        if getattr(game, 'word_id', None) is not None:
            # fetch the word
            w = session.get(models.Word, game.word_id)
            # only build metadata if word found
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
        'initial_attempts': game.initial_attempts,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'hints_used': getattr(game, 'hints_used', 0),
        'word': word_meta,
    }
    # Return the active game back to the frontend
    return response


# Endpoint to start a new game
@router.post("/new", response_model=schemas.GameRead)
def new_game(payload: schemas.GameCreate, session: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    """Create a new game for the authenticated user. Requires a valid Bearer token."""
    # fetch a random word based on topic and difficulty
    word = crud.get_random_word(session, payload.topic, payload.difficulty)
    # validate word found
    if not word:
        # no word found matching criteria
        raise HTTPException(status_code=404, detail="No words available")

    # determine initial attempts based on difficulty
    difficulty_attempts_map = {
        'easy': 5,
        'medium': 7,
        'hard': 9,
        'insane': 10,
    }
    # default to 6 attempts if difficulty not recognized
    initial_attempts = difficulty_attempts_map.get(payload.difficulty, 6)

    # current_user is provided by get_current_user and will raise 401 if auth is missing/invalid
    game = crud.create_game(session, current_user, word, initial_attempts=initial_attempts)
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
    # Build the response payload
    response = {
        'id': game.id,
        'revealed': game.revealed,
        'initial_attempts': game.initial_attempts,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'hints_used': getattr(game, 'hints_used', 0),
        'word': word_meta,
    }
    # Return the new game back to the frontend
    return response


# Endpoint to get a game by id (used for resume)
@router.get("/{game_id}", response_model=schemas.GameRead)
def get_game(game_id: int, session: Session = Depends(get_session), authorization: Optional[str] = Header(None)):
    '''Get a game by ID. If Authorization header is provided, ensure the caller owns the game.'''
    # fetch the game by id
    game = session.get(models.Game, game_id)
    # validate game found
    if not game:
        # Raise 404 if game not found
        raise HTTPException(status_code=404, detail="Game not found")
    # If an Authorization header is present, ensure the caller owns the game
    user = try_get_user_from_header(authorization, session)
    # if user is resolved, check ownership
    if user and game.user_id != user.id:
        # caller does not own this game
        raise HTTPException(status_code=403, detail="Not allowed to access this game")

    # Build explicit response that contains only word metadata (no word.text) so that user can't cheat
    word_meta = None
    # attempt to build word metadata
    try:
        # only attempt if word_id is present
        if getattr(game, 'word_id', None) is not None:
            # fetch the word
            w = session.get(models.Word, game.word_id)
            # only build metadata if word found
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
        'initial_attempts': game.initial_attempts,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'hints_used': getattr(game, 'hints_used', 0),
        'word': word_meta,
    }
    # Return the game back to the frontend
    return response


# Endpoint to make a guess in an existing game
@router.post("/{game_id}/guess", response_model=schemas.GameRead)
def guess(game_id: int, payload: schemas.GuessIn, session: Session = Depends(get_session)):
    '''Make a guess for the specified game.'''
    # fetch the game by id
    game = session.get(models.Game, game_id)
    # validate game found
    if not game:
        # Raise 404 if game not found
        raise HTTPException(status_code=404, detail="Game not found")

    # Only allow guesses when the game is actively in progress otherwise return 409 Conflict
    if game.state != 'active':
        # Game already finished (won/lost) or otherwise inactive - inform the client
        raise HTTPException(status_code=409, detail=f"Game is not active (state={game.state}). Start a new game to continue.")

    # Validate the letter input
    word = session.get(models.Word, game.word_id)
    # get the guessed letter in lowercase
    letter = payload.letter.lower()
    # normalize guessed storage
    guessed_set = set((game.guessed or '').lower()) if game.guessed is not None else set()
    # validate single alphabetic character
    if letter in guessed_set:
        # Letter has already been guessed; don't apply scoring or change attempts
        raise HTTPException(status_code=409, detail=f"Letter '{letter}' was already guessed")
    # validate single character
    if letter in word.text.lower():
        # reveal occurrences
        new = list(game.revealed)
        # reveal all occurrences of the letter
        for i, ch in enumerate(word.text.lower()):
            # match found
            if ch == letter:
                new[i] = word.text[i]
        # update revealed word
        game.revealed = "".join(new)
        # simple scoring
        # increase score only for newly discovered occurrences
        game.score += word.text.lower().count(letter) * 10
        # record guessed letter
        guessed_set.add(letter)
        # update guessed letters
        game.guessed = ''.join(sorted(guessed_set))
    else:
        # incorrect guess
        # decrease attempts left
        game.attempts_left -= 1
        # record guessed letter even if incorrect
        guessed_set.add(letter)
        # update guessed letters
        game.guessed = ''.join(sorted(guessed_set))
        # check if game is lost
        if game.attempts_left <= 0:
            game.state = "lost"

    # check win condition
    if "_" not in game.revealed:
        # set the game state to won
        game.state = "won"

    # save the game state
    session.add(game)
    session.commit()
    session.refresh(game)

    # Build explicit response that contains only word metadata (no word.text) so that user can't cheat
    word_meta = None
    # attempt to build word metadata
    try:
        # only attempt if word_id is present
        if getattr(game, 'word_id', None) is not None:
            # fetch the word
            w = session.get(models.Word, game.word_id)
            # only build metadata if word found
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
        'initial_attempts': game.initial_attempts,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'state': game.state,
        'guessed': game.guessed,
        'hints_used': game.hints_used,
        'word': word_meta,
    }
    # return the updated game state back to the frontend
    return response


@router.post("/{game_id}/hint", response_model=schemas.GameRead)
def use_hint(game_id: int, session: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    """Use a hint for the specified game."""
    # fetch the game by id
    game = session.get(models.Game, game_id)
    # validate game found
    if not game:
        # Raise 404 if game not found
        raise HTTPException(status_code=404, detail="Game not found")

    # Ensure the current user owns this game
    if game.user_id != current_user.id:
        # caller does not own this game
        raise HTTPException(status_code=403, detail="Not your game")

    # Only allow hints when the game is actively in progress
    if game.state != 'active':
        # Game already finished (won/lost) or otherwise inactive - inform the client
        raise HTTPException(status_code=409, detail="Game is not active")

    # Fetch the word associated with the game
    word = session.get(models.Word, game.word_id)
    # validate word found
    if not word:
        # Word not found
        raise HTTPException(status_code=404, detail="Word not found for this game")

    # Find a letter that has not been revealed yet
    unrevealed_indices = [i for i, char in enumerate(game.revealed) if char == '_']
    # if no unrevealed letters, cannot provide a hint
    if not unrevealed_indices:
        # No more letters to reveal
        raise HTTPException(status_code=400, detail="No more letters to reveal")

    # randomly select one unrevealed letter to reveal
    import random
    # randomly select one unrevealed letter to reveal
    index_to_reveal = random.choice(unrevealed_indices)
    # get the letter at that index
    letter_to_reveal = word.text[index_to_reveal]

    # Update the revealed word
    revealed_list = list(game.revealed)
    # reveal all occurrences of the selected letter
    for i, char in enumerate(word.text):
        # match found
        if char == letter_to_reveal:
            # reveal the letter
            revealed_list[i] = char
    # update the revealed word
    game.revealed = "".join(revealed_list)

    # Apply penalty and update hints used
    game.score -= 10
    game.hints_used += 1

    # Add the revealed letter to the guessed letters
    guessed_set = set((game.guessed or '').lower())
    # add the revealed letter
    guessed_set.add(letter_to_reveal.lower())
    # update guessed letters
    game.guessed = ''.join(sorted(list(guessed_set)))

    # Check for win condition
    if "_" not in game.revealed:
        # set the game state to won
        game.state = "won"

    # Save the updated game state
    session.add(game)
    session.commit()
    session.refresh(game)

    # Build explicit response that contains only word metadata (no word.text) so that user can't cheat
    word_meta = {
        'id': word.id,
        'clue': word.clue,
        'topic': word.topic,
        'difficulty': word.difficulty,
    }
    # Build the response payload
    response = {
        'id': game.id,
        'revealed': game.revealed,
        'initial_attempts': game.initial_attempts,
        'attempts_left': game.attempts_left,
        'score': game.score,
        'hints_used': game.hints_used,
        'state': game.state,
        'guessed': game.guessed,
        'word': word_meta,
    }
    # return the updated game state back to the frontend
    return response
