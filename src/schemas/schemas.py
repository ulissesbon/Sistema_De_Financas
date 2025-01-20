from typing import Optional, List
from pydantic import BaseModel
from datetime import date


class CategoriaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    tipo: bool

    class Config:
        orm_mode = True


class GanhosSchema(BaseModel):
    id: Optional[int] = None
    descricao: Optional[str] = 'Sem descrição!'
    valor: float
    data: date
    categoria_id: Optional[int] = None

    class Config:
        orm_mode = True


class GastosSchema(BaseModel):
    id: Optional[int] = None
    descricao: Optional[str] = 'Sem descrição!'
    valor: float
    data: date
    categoria_id: Optional[int] = None

    class Config:
        orm_mode = True


class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    senha: str

    class Config:
        orm_mode = True


class UsuarioSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str

    class Config:
        orm_mode = True


class LoginData(BaseModel):
    senha: str
    email: str

class LoginSucess(BaseModel):
    usuario_login: UsuarioSimples
    acess_token: str
