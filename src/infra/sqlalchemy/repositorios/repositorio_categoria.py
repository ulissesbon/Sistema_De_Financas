from src.infra.sqlalchemy.models import models
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.schemas import schemas
from typing import List

class RepositorioCategoria():
    def __init__(self, db: Session):
        self.db = db

    def criar(self, categoria: schemas.CategoriaSchema):
        db_categoria = models.CategoriaModel(
            nome = categoria.nome,
            tipo = categoria.tipo
        )
    
        self.db.add(db_categoria)
        self.db.commit()
        self.db.refresh(db_categoria)
        
        return db_categoria
    
    def listar_categorias(self):
        categorias = self.db.query(models.CategoriaModel).all()
        return categorias
    
    def obter(self, categoria_id: int) -> models.CategoriaModel:
        stmt = select(models.CategoriaModel).filter_by(id=categoria_id)
        categoria = self.db.execute(stmt).one()

        return categoria
    
    def remover(self, categoria_id: int):
        stmt = delete(models.CategoriaModel).where(models.CategoriaModel.id == categoria_id)

        self.db.execute(stmt)
        self.db.commit()
        
    def editar(self, categoria_id: int, categoria: schemas.CategoriaSchema):
        
        categoria_existente = self.db.query(models.CategoriaModel).filter(models.CategoriaModel.id == categoria.id).first()
        if not categoria_existente:
            raise HTTPException(status_code=404, detail= "Categoria não encontrada")

        update_stmt = update(models.CategoriaModel
                             ).where(models.CategoriaModel.id == categoria_id
                                     ).values(
                                         nome = categoria.nome,
                                         tipo = categoria.tipo
                                     )

        self.db.execute(update_stmt)
        self.db.commit()
        