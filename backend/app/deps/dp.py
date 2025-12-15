from typing import Generator
from sqlmodel import Session
from ..database import engine

# Dependency to get a database session
def get_session() -> Generator[Session, None, None]:
    # Create a new session
    with Session(engine) as session:
        # Yield the session to be used in the request
        yield session

__all__ = ["get_session"]

