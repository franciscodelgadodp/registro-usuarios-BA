from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from utils.db import Base


user_scope_association_table = Table(
    "scope_user",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("scope_id", ForeignKey("scopes.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True)
    estado = Column(String)
    municipio = Column(String)
    curp = Column(String, unique=True)
    rfc = Column(String, unique=True)
    telefono = Column(BigInteger)
    cp = Column(Integer)
    fecha_nacimiento = Column(String)
    contraseña = Column(String)

    scopes = relationship(
        "Scope", secondary=user_scope_association_table
    )


class Scope(Base):
    __tablename__ = "scopes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
