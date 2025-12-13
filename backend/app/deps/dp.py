from typing import Generator
from sqlmodel import Session
from ..database import engine

# Dependency to get a database session
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

__all__ = ["get_session"]

