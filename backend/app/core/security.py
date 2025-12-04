from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# Security settings
SECRET_KEY = "9fH3bVqX7wZ2LpA9s8RkYt1mN4uJ6eC0oS-3vGzQ5xT_cW8yF2hM7nP0aL1bR6sE9uK"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create a JWT access token
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    '''
    This function creates a JWT access token for the given subject with an optional expiration time.
    :param subject: The subject (usually user identifier) for whom the token is created
    :param expires_delta: Optional timedelta for token expiration
    :return: Encoded JWT access token as a string
    '''

    to_encode = {"sub": str(subject)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify a plain password against a hashed password
def verify_password(plain_password, hashed_password) -> bool:
    '''
    This function verifies a plain password against a hashed password.
    :param plain_password: Plain text password to verify
    :param hashed_password: Hashed password to compare against
    :return: True if the password matches, False otherwise
    '''

    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a plain password
def get_password_hash(password) -> str:
    '''
    This function hashes the provided password using bcrypt algorithm.
    :param password: Plain text password to be hashed
    :return: Hashed password string
    '''

    return pwd_context.hash(password)

