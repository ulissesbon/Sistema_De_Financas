from sqlalchemy import Date, Integer, Column, String, Float, ForeignKey, Boolean
from src.infra.sqlalchemy.config.database import Base
from sqlalchemy.orm import relationship


class CategoriaModel(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tipo = Column(Boolean) #True = ganhos / False = gastos


class GanhosModel(Base):
    __tablename__ = 'ganhos'

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Float)
    data = Column(Date)
    categoria_id = Column(Integer, ForeignKey('categoria.id', name='fk_categoria'))

    categoria = relationship('Categoria', back_populates='ganhos')


class GastosModel(Base):
    __tablename__ = 'gastos'

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Float)
    data = Column(Date)
    categoria_id = Column(Integer, ForeignKey('categoria.id', name='fk_categoria'))

    categoria = relationship('Categoria', back_populates='gastos')
    

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
