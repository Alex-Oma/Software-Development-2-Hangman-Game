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


class GameRead(BaseModel):
    # Game read schema
    id: int
    revealed: Optional[str]
    attempts_left: int
    score: int
    state: str

    class Config:
        # Enable ORM mode for compatibility with SQLModel
        orm_mode = True

