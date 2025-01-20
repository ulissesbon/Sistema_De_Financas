from src.infra.sqlalchemy.models import models
from sqlalchemy import delete, select, update
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.schemas import schemas
from typing import List

class RepositorioGastos():
    def __init__(self, db: Session):
        self.db = db


    def criar(self, gasto: schemas.GastosSchema):
        db_gasto = models.GastosModel(
            descricao = gasto.descricao,
            valor = gasto.descricao,
            data = gasto.data,
            categoria_id = gasto.categoria_id
        )

        self.db.add(db_gasto)
        self.db.commit()
        self.db.refresh(db_gasto)

        return db_gasto
    

    def listar_gastos(self):
        gastos = self.db.query(models.GastosModel).all()
        return gastos
    

    def obter_gastor(self, gasto_id: int):
        stmt = select(models.GastosModel).filter_by(id = gasto_id)
        gasto = self.db.execute(stmt).one()
        return gasto[0]
    

    def remover(self, gasto_id: int):
        stmt = delete(models.GastosModel).where(models.GastosModel.id == gasto_id)

        self.db.execute(stmt)
        self.db.commit()
        

    def editar(self, gasto_id: int, gasto: schemas.GastosSchema):

        gasto_existente = self.db.query(models.GastosModel).filter(models.GastosModel.id == gasto_id).first()
        if not gasto_existente:
            raise HTTPException(status_code=404, detail= "Gasto não encontrado")
        
        update_stmt = update(models.GastosModel
                             ).where(models.GastosModel.id == gasto_id
                                     ).values(
                                         descricao = gasto.descricao,
                                         valor = gasto.valor,
                                         data = gasto.data,
                                         categoria_id = gasto.categoria_id
                                     )
        
        self.db.execute(update_stmt)
        self.db.commit()


    def listar_gastos_categoria(self, id_categoria: int):
        query = select(models.GastosModel).where(models.GastosModel.categoria_id == id_categoria)
        resultado = self.db.execute(query).scalars().all()

        return resultado
    
    
    def listar_gastos_intervalo_data(self, data_inicio: date, data_final: date):
        query = select(models.GastosModel).where(models.GastosModel.data >= data_inicio and models.GastosModel.data <= data_final)
        resultado = self.db.execute(query).scalars().all()

        return resultado