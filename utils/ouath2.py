from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from utils.db import get_db

from . import token as tokenModule


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={})


async def get_current_user(security_scopes: SecurityScopes, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las crendenciales",
        headers={"WWW-Authenticate": authenticate_value},
    )

    return await tokenModule.verify_token(token, credentials_exception, db, security_scopes.scopes)
