from src.infra.sqlalchemy.repositorios.repositorio_categoria import RepositorioCategoria
from src.schemas.schemas import UsuarioSchema, CategoriaSchema
from fastapi import HTTPException, APIRouter, Depends, status
from src.routers.auth_utils import obter_usuario_logado
from src.infra.sqlalchemy.config.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/categorias')


@router.post('/add', status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria= CategoriaSchema, usuario: UsuarioSchema= Depends(obter_usuario_logado), db: Session = Depends(get_db)):

    categoria_criada = RepositorioCategoria(db).criar(categoria)
    categoria_criada.usu = usuario.id

    return categoria_criada

