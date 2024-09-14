 
from sqlalchemy import Column, Integer, String
from models.mapping import Base
from sqlalchemy.orm import relationship

class CategoriaMercado(Base):
    __tablename__ = 'categoria_mercado' 
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    
    criptos = relationship("DimCripto", back_populates="categoria")
    fato_cripto = relationship("FatoCripto", back_populates="categoria")

    def __init__(self, id: int, descricao: str):
        self.id = id
        self.descricao = descricao