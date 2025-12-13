from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# Security settings
SECRET_KEY = "9fH3bVqX7wZ2LpA9s8RkYt1mN4uJ6eC0oS-3vGzQ5xT_cW8yF2hM7nP0aL1bR6sE9uK"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

# Use a PBKDF2-based scheme by default to avoid system bcrypt dependency issues
# pbkdf2_sha256 is widely supported and avoids bcrypt's 72-byte limit and binary build
# Keep bcrypt_sha256 and bcrypt as fallbacks if a bcrypt backend is available and desired.
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt_sha256", "bcrypt"], deprecated="auto")

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
    This function hashes the provided password using a secure PBKDF2/SHA-256 based algorithm
    by default to avoid bcrypt binary dependency issues. If you prefer bcrypt, install and configure
    a compatible bcrypt backend and adjust the CryptContext schemes order.
    :param password: Plain text password to be hashed
    :return: Hashed password string
    '''

    return pwd_context.hash(password)
