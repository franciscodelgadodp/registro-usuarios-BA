from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from adapters import sql_alchemy_orm as orm
from utils.db import get_db
from utils.hashing import verify
from utils.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


router = APIRouter(
    prefix="/token",
    tags=["authentication"],
)


@router.post("/", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # try:
    user: orm.User = db.query(orm.User).filter(
        orm.User.correo == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no existe")
    if not verify(user.contraseña, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credenciales invalidas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = [scope.name for scope in user.scopes]
    access_token = create_access_token(
        data={"sub": user.id, "email": user.correo, "scopes": scopes}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

    # except:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
