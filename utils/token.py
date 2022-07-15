from datetime import datetime, timedelta
from typing import Union
from sqlalchemy.orm import Session

from fastapi import HTTPException

from jose import JWTError, jwt

from models.auth import TokenData


SECRET_KEY = "7870ee77ef46443b4dcd022557487fb7d67eea429935efe93f3bcd27802106ae"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def format_scope(scope):
    scope_split = scope.split(":")
    if len(scope_split) > 1:
        scope_split[2] = scope_split[2].split(",")
    return scope_split


async def verify_token(token: str, credentials_exception: HTTPException, db: Session, required_scopes: list[str]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])

        if not token_scopes:
            raise credentials_exception

        token_data = TokenData(scopes=token_scopes, username=username)

        if "admin" in token_data.scopes:

            return token_data

        token_scopes = list(map(format_scope, token_scopes))

        scopes = [f"{scope[0]}:{scope[1]}" for scope in token_scopes]

        if all(elem in scopes for elem in required_scopes):
            return token_data

        raise credentials_exception
    except JWTError:
        raise credentials_exception
