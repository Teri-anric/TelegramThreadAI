"""
Access token utilities.
"""

from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status

from app.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token

    :param data: The data to encode in the token
    :param expires_delta: Optional time delta for token expiration
    """
    to_encode = data.copy()

    if not expires_delta:
        expires_delta = timedelta(seconds=settings.jwt.access_token_expire_seconds)
    expire = datetime.now(UTC) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token

    :param token: The JWT token to decode
    :return: The decoded payload
    """
    try:
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
