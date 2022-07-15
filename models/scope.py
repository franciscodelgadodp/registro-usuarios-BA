from pydantic import BaseModel


class ScopeBase(BaseModel):
    name: str


class ScopeCreate(ScopeBase):
    pass


class Scope(ScopeBase):
    id: str

    class Config:
        orm_mode = True
