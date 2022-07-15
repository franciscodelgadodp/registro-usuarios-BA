from fastapi import Depends, status, HTTPException, APIRouter, Security
from sqlalchemy.orm import Session

from models.user import User, UserCreate, UserUpdate
from services.user_services import create_user_service, delete_user_service, list_users_service, get_user_service, update_user_service
from utils.db import get_db
from utils.ouath2 import get_current_user


router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[User])
async def list_users(page: int = 0, limit: int = 10, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["user:read"])):
    return list_users_service(db, page, limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["user:create"])):
    return create_user_service(user, db)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: str, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["user:read"])):
    user = get_user_service(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario no existe")
    return user


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=User)
async def update_user(user_id: str, updated_user: UserUpdate, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["user:update"])):
    return update_user_service(user_id, updated_user, db, get_current_user, ["user", "update"])


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["user:delete"])):
    try:
        return delete_user_service(user_id, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
