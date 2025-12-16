import sys
from pathlib import Path

# Ensure the repository root is on sys.path so imports like `backend.app` work
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from backend.app.main import app
from backend.app.deps import get_session
# Import all models to ensure tables are created
from backend.app.models import models as app_models
from backend.app.models.models import User, Word, Game


# In-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_session():
    """Provide a test database session."""
    with Session(engine) as session:
        yield session


# Override the dependency to use the test database
app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(name="client")
def client_fixture():
    """
    Pytest fixture to provide a TestClient for the FastAPI app.
    This handles creating and tearing down the database for each test session.
    """
    SQLModel.metadata.create_all(engine, tables=[User.__table__, Word.__table__, Game.__table__])
    with TestClient(app) as client:
        yield client
    SQLModel.metadata.drop_all(engine)
