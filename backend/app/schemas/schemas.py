from typing import Optional
from pydantic import BaseModel

# Pydantic models for request and response schemas
class UserCreate(BaseModel):
    '''
    Schema for creating a new user.
    '''
    # User creation schema
    username: str
    email: Optional[str] = None
    password: str


class UserRead(BaseModel):
    '''
    Schema for reading user information.
    '''
    # User read schema
    id: int
    username: str
    email: Optional[str]

    # Enable ORM mode for compatibility with SQLModel
    class Config:
        orm_mode = True


class Token(BaseModel):
    '''
    Schema for authentication token.
    '''
    # Token schema for authentication
    access_token: str
    token_type: str = "bearer"


class GameCreate(BaseModel):
    '''
    Schema for creating a new game with optional filters.
    '''
    # Game creation schema with optional filters
    topic: Optional[str] = None
    difficulty: Optional[str] = None


class GuessIn(BaseModel):
    '''
    Schema for a letter guess input.
    '''
    # Guess input schema
    letter: str


class WordMeta(BaseModel):
    """Metadata about a word exposed to clients (no actual word text included)."""
    id: Optional[int]
    clue: Optional[str]
    topic: Optional[str]
    difficulty: Optional[str]

    # Enable ORM mode for compatibility with SQLModel
    class Config:
        orm_mode = True


class GameRead(BaseModel):
    '''
    Schema for reading game information.
    '''
    # Game read schema
    id: int
    revealed: Optional[str]
    initial_attempts: int
    attempts_left: int
    score: int
    hints_used: int
    state: str
    guessed: Optional[str]
    # include nested word metadata (no actual word text) so frontend can show clue/topic but not the answer
    word: Optional[WordMeta] = None

    class Config:
        # Enable ORM mode for compatibility with SQLModel
        orm_mode = True
