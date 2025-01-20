from src.infra.sqlalchemy.models import models
from sqlalchemy import delete, select, update
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.schemas import schemas
from typing import List

class RepositorioGanhos():
    def __init__(self, db: Session):
        self.db = db


    def criar(self, ganho: schemas.GanhosSchema):
        db_ganho = models.GanhosModel(
            descricao = ganho.descricao,
            valor = ganho.descricao,
            data = ganho.data,
            categoria_id = ganho.categoria_id
        )

        self.db.add(db_ganho)
        self.db.commit()
        self.db.refresh(db_ganho)

        return db_ganho
    

    def listar_ganhos(self):
        ganhos = self.db.query(models.GanhosModel).all()
        return ganhos
    

    def obter_ganhor(self, ganho_id: int):
        stmt = select(models.GanhosModel).filter_by(id = ganho_id)
        ganho = self.db.execute(stmt).one()
        return ganho[0]
    

    def remover(self, ganho_id: int):
        stmt = delete(models.GanhosModel).where(models.GanhosModel.id == ganho_id)

        self.db.execute(stmt)
        self.db.commit()
        

    def editar(self, ganho_id: int, ganho: schemas.GanhosSchema):

        ganho_existente = self.db.query(models.GanhosModel).filter(models.GanhosModel.id == ganho_id).first()
        if not ganho_existente:
            raise HTTPException(status_code=404, detail= "Ganho não encontrado")
        
        update_stmt = update(models.GanhosModel
                             ).where(models.GanhosModel.id == ganho_id
                                     ).values(
                                         descricao = ganho.descricao,
                                         valor = ganho.valor,
                                         data = ganho.data,
                                         categoria_id = ganho.categoria_id
                                     )
        
        self.db.execute(update_stmt)
        self.db.commit()


    def listar_ganhos_categoria(self, id_categoria: int):
        query = select(models.GanhosModel).where(models.GanhosModel.categoria_id == id_categoria)
        resultado = self.db.execute(query).scalars().all()

        return resultado
    
    
    def listar_ganhos_intervalo_data(self, data_inicio: date, data_final: date):
        query = select(models.GanhosModel).where(models.GanhosModel.data >= data_inicio and models.GanhosModel.data <= data_final)
        resultado = self.db.execute(query).scalars().all()

        return resultado