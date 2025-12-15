from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from .. import schemas, crud
from ..deps import get_session
from ..core import security

# Define the API router for authentication
router = APIRouter()

# Endpoint for user registration
@router.post("/register", response_model=schemas.UserRead)
def register(payload: schemas.UserCreate, session: Session = Depends(get_session)):
    # Check if username already exists
    existing = crud.get_user_by_username(session, payload.username)
    # If it does, raise an error
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    # Create the user
    user = crud.create_user(session, payload.username, payload.email, payload.password)
    # Return the created user back to the frontend
    return user

# Endpoint for user login
@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserCreate, session: Session = Depends(get_session)):
    # Retrieve the user by username
    user = crud.get_user_by_username(session, payload.username)
    # Verify the password
    if not user or not security.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Create an access token for the user
    token = security.create_access_token(subject=str(user.id))
    # Return the token to the frontend
    return schemas.Token(access_token=token)

