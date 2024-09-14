from models.mapping import Base 
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship

class FatoCripto(Base):
    __tablename__ = 'fato_criptos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    preco_atual = Column(Numeric, nullable=False)
    categoria_preco = Column(String(10), nullable=False)

    idCripto = Column(Integer, ForeignKey('dim_criptos.id'), nullable=False)
    idCategoria = Column(Integer, ForeignKey('categoria_mercado.id'), nullable=False)

    cripto = relationship("DimCripto", back_populates="fato_cripto")
    categoria = relationship("CategoriaMercado", back_populates="fato_cripto")
    
    def __init__(self, idCripto: int, data: str, preco_atual: float, categoria_preco: str, idCategoria: int):
        self.idCripto = idCripto
        self.data = data
        self.preco_atual = preco_atual
        self.categoria_preco = categoria_preco
        self.idCategoria = idCategoria