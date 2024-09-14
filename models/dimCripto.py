 
from sqlalchemy import Column, Integer, String, ForeignKey
from models.mapping import Base
from sqlalchemy.orm import relationship

class DimCripto(Base):
    __tablename__ = 'dim_criptos' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    simbolo = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    idCategoria = Column(Integer, ForeignKey('categoria_mercado.id'), nullable=False)
    
    categoria = relationship("CategoriaMercado", back_populates="criptos")
    fato_cripto = relationship("FatoCripto", back_populates="cripto")

    def __init__(self, nome: str, simbolo: str, rank: int, idCategoria: int):
        self.nome = nome
        self.simbolo = simbolo
        self.rank = rank
        self.idCategoria = idCategoria