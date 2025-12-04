from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///./hangman.db"

engine = create_engine(DATABASE_URL, echo=False)

