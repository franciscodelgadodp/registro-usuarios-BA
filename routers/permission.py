from fastapi import Depends, status, HTTPException, APIRouter, Security
from sqlalchemy.orm import Session
from models.scope import Scope, ScopeCreate

from models.user import User, UserCreate, UserUpdate
from services.permission_services import create_scope_service, delete_scope_service, get_scope_service, list_scopes_service, update_scope_service
from utils.db import get_db
from utils.ouath2 import get_current_user


router = APIRouter(
    prefix="/scope",
    tags=["scopes"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Scope])
async def list_scopes(page: int = 0, limit: int = 10, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["scope:read"])):
    return list_scopes_service(db, page, limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Scope)
async def create_scope(scope: ScopeCreate, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["scope:create"])):
    return create_scope_service(scope, db)


@router.get("/{scope_id}", status_code=status.HTTP_200_OK, response_model=Scope)
async def get_scope(scope_id: str, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["scope:read"])):
    scope = get_scope_service(scope_id, db)
    if not scope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Scope no existe")
    return scope


@router.put("/{scope_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_scope(scope_id: str, updated_scope: ScopeCreate, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["scope:update"])):
    return update_scope_service(scope_id, updated_scope, db)


@router.delete("/{scope_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scope(scope_id: str, db: Session = Depends(get_db), get_current_user: User = Security(get_current_user, scopes=["scope:delete"])):
    try:
        return delete_scope_service(scope_id, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
