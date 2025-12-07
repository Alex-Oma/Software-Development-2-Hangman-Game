from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from .. import schemas, crud, models
from ..deps import get_session

# Router for game-related endpoints
router = APIRouter()

# Endpoint to start a new game
@router.post("/new", response_model=schemas.GameRead)
def new_game(payload: schemas.GameCreate, session: Session = Depends(get_session)):
    word = crud.get_random_word(session, payload.topic, payload.difficulty)
    if not word:
        raise HTTPException(status_code=404, detail="No words available")
    # temporary anonymous user (id=1) support for skeleton
    user: Optional[models.User] = session.get(models.User, 1)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Register a user first.")
    game = crud.create_game(session, user, word)
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
