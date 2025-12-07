import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app import models
from backend.app.deps import get_session as real_get_session


@pytest.fixture
def in_memory_client():
    # create an in-memory SQLite engine for tests that is shareable across threads
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    # override the dependency
    app.dependency_overrides[real_get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    # cleanup override
    app.dependency_overrides.pop(real_get_session, None)


def test_register_and_login_flow(in_memory_client):
    client = in_memory_client
    username = "testuser"
    password = "testpass"

    # Register
    r = client.post("/api/auth/register", json={"username": username, "email": "u@example.com", "password": password})
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == username
    assert "id" in data

    # Login
    r2 = client.post("/api/auth/login", json={"username": username, "password": password})
    assert r2.status_code == 200
    token = r2.json().get("access_token")
    assert token and isinstance(token, str)


def test_register_duplicate_user(in_memory_client):
    client = in_memory_client
    username = "dupuser"
    password = "abc123"

    r = client.post("/api/auth/register", json={"username": username, "email": "dup@example.com", "password": password})
    assert r.status_code == 200

    # Register again should fail
    r2 = client.post("/api/auth/register", json={"username": username, "email": "dup2@example.com", "password": password})
    assert r2.status_code == 400
    assert r2.json().get("detail") == "Username already exists"


def test_login_wrong_credentials(in_memory_client):
    client = in_memory_client
    username = "userx"
    password = "mypassword"

    # prepare by registering
    r = client.post("/api/auth/register", json={"username": username, "email": "x@example.com", "password": password})
    assert r.status_code == 200

    # Try login with wrong password
    r2 = client.post("/api/auth/login", json={"username": username, "password": "wrong"})
    assert r2.status_code == 401
    assert r2.json().get("detail") == "Invalid credentials"
