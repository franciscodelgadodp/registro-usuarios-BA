
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from adapters import sql_alchemy_orm

from models.user import UserCreate, User
from adapters.sql_alchemy_orm import User as UserOrm, Scope
from utils.hashing import bcrypt
from utils.token import format_scope
from utils.validations import validar_cp, validar_curp, validar_estado, validar_fecha, validar_municipio, validar_rfc, validar_telefono
# from utils.token import format_scope


def _validar_datos(user: UserCreate):
    if not validar_curp(user.curp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"CURP {user.curp} no es válida")
    if not validar_rfc(user.rfc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"RFC {user.rfc} no es válida")
    if not validar_cp(user.cp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"CP {user.cp} no es válido")
    if not validar_fecha(user.fecha_nacimiento):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fecha {user.fecha_nacimiento} no es válida")
    if not validar_telefono(user.telefono):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Teléfono {user.telefono} no es válido")
    if not validar_estado(user.estado):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Estado {user.estado} no es válido")
    if not validar_municipio(user.estado, user.municipio):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Municipio {user.municipio} no es válido")


def create_user_service(user: UserCreate, db: Session):
    # Validar datos
    _validar_datos(user)

    try:
        contraseña = bcrypt(user.contraseña)
        if user.scopes:
            user.scopes = [db.query(Scope).get(id) for id in user.scopes]

        new_user = UserOrm(id=str(uuid4()), nombre=user.nombre, estado=user.estado, correo=user.correo,
                           municipio=user.municipio, curp=user.curp, rfc=user.rfc, telefono=user.telefono,
                           cp=user.cp, fecha_nacimiento=user.fecha_nacimiento, contraseña=contraseña,
                           scopes=user.scopes)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


def list_users_service(db: Session, page: int, limit: int):
    try:
        offset = page*limit
        users = db.query(UserOrm).limit(10).offset(offset).all()
        return users
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


def get_user_service(user_id: str, db: Session):
    try:
        user = db.query(UserOrm).get(user_id)
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


def delete_user_service(user_id: str, db: Session):
    user = db.query(UserOrm).get(user_id)
    db.delete(user)
    db.commit()
    return


def update_user_service(user_id: str, updated_user: UserCreate, db: Session, current_user: object, scopes: list[str]):
    user: UserOrm = get_user_service(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario no existe")
    _validar_datos(updated_user)

    permission_attributes = []

    if "admin" in current_user.scopes:
        token_scopes = current_user.scopes
    else:
        token_scopes = list(map(format_scope, current_user.scopes))

        for token in token_scopes:
            if token[0] == scopes[0] and token[1] == scopes[1]:
                permission_attributes = token[2]

    user_dict = user.__dict__

    for key, value in updated_user.dict().items():
        if key == "scopes":
            if value:
                if "scopes" in token_scopes:
                    value = [db.query(Scope).get(id) for id in value]
                    setattr(user, key, value)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Usuario no autorizado para modificar {key}")
        elif user_dict[key] != value:
            if ("admin" in token_scopes) or (key in permission_attributes) or ("*" in permission_attributes):
                setattr(user, key, value)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Usuario no autorizado para modificar {key}")
    try:
        db.commit()
        db.refresh(user)
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
