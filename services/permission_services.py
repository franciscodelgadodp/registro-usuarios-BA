
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from models.scope import ScopeCreate

from adapters.sql_alchemy_orm import Scope as ScopeORM


def create_scope_service(scope: ScopeCreate, db: Session):

    try:
        new_scope = ScopeORM(id=str(uuid4()), name=scope.name)
        db.add(new_scope)
        db.commit()
        db.refresh(new_scope)
        return new_scope
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


def list_scopes_service(db: Session, page: int, limit: int):
    try:
        offset = page*limit
        scopes = db.query(ScopeORM).limit(10).offset(offset).all()
        return scopes
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


def get_scope_service(scope_id: str, db: Session):
    try:
        scope = db.query(ScopeORM).get(scope_id)
        return scope
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


def delete_scope_service(scope_id: str, db: Session):
    scope = db.query(ScopeORM).get(scope_id)
    db.delete(scope)
    db.commit()
    return


def update_scope_service(scope_id: str, updated_scope: ScopeCreate, db: Session):
    scope: ScopeORM = get_scope_service(scope_id, db)
    if not scope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario no existe")

    scope_dict = scope.__dict__

    for key, value in updated_scope.dict().items():
        if scope_dict[key] != value:
            setattr(scope, key, value)

    try:
        db.commit()
        db.refresh(scope)
        return scope
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
