from pydantic import BaseModel


class UserBase(BaseModel):
    nombre: str
    curp: str
    correo: str
    estado: str
    municipio: str
    rfc: str
    telefono: int
    cp: int
    fecha_nacimiento: str


class UserCreate(UserBase):
    contraseña: str
    scopes: list[str] = []


class UserUpdate(UserBase):
    scopes: list[str] = []


class User(UserBase):
    id: str

    class Config:
        orm_mode = True
