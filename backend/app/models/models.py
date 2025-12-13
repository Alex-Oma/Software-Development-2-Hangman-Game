from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Define the User, Word, and Game models

class User(SQLModel, table=True):
    '''
    User model representing a player in the Hangman game.
    '''
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str] = None
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    games: List["Game"] = Relationship(back_populates="user")


class Word(SQLModel, table=True):
    '''
    Word model representing a word to be guessed in the Hangman game.
    '''
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    clue: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None


class Game(SQLModel, table=True):
    '''
    Game model representing a Hangman game session.
    '''
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    word_id: Optional[int] = Field(foreign_key="word.id")
    revealed: Optional[str] = Field(default=None)
    # guessed letters stored as a compact lowercase string (e.g. 'aei')
    guessed: Optional[str] = Field(default='')
    attempts_left: int = Field(default=6)
    score: int = Field(default=0)
    state: str = Field(default="active")  # active/won/lost
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="games")
    word: Optional[Word] = Relationship()
