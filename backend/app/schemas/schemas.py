from typing import Optional
from pydantic import BaseModel

# Pydantic models for request and response schemas
class UserCreate(BaseModel):
    # User creation schema
    username: str
    email: Optional[str] = None
    password: str


class UserRead(BaseModel):
    # User read schema
    id: int
    username: str
    email: Optional[str]

    class Config:
        orm_mode = True


class Token(BaseModel):
    # Token schema for authentication
    access_token: str
    token_type: str = "bearer"


class GameCreate(BaseModel):
    # Game creation schema with optional filters
    topic: Optional[str] = None
    difficulty: Optional[str] = None


class GuessIn(BaseModel):
    # Guess input schema
    letter: str


class WordMeta(BaseModel):
    """Metadata about a word exposed to clients (no actual word text included)."""
    id: Optional[int]
    clue: Optional[str]
    topic: Optional[str]
    difficulty: Optional[str]

    class Config:
        orm_mode = True


class GameRead(BaseModel):
    # Game read schema
    id: int
    revealed: Optional[str]
    attempts_left: int
    score: int
    state: str
    guessed: Optional[str]
    # include nested word metadata (no actual word text) so frontend can show clue/topic but not the answer
    word: Optional[WordMeta] = None

    class Config:
        # Enable ORM mode for compatibility with SQLModel
        orm_mode = True
