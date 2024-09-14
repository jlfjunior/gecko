import uvicorn
from fastapi import FastAPI
from models.fatoCripto import FatoCripto
from models.categoriaMercado import CategoriaMercado
from models.dimCripto import DimCripto
from services.geckoService import GeckoService
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.mapping import Base
import datetime as dt

app = FastAPI()
engine = sqlalchemy.create_engine('sqlite:///gecko.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def seed():
    exists = session.query(CategoriaMercado).count()

    if exists == 0:
        c1 = CategoriaMercado(1, "Low")
        c2 = CategoriaMercado(2, "Medium")  
        c3 = CategoriaMercado(3, "High")
        
        session.add_all([c1, c2, c3])
        session.commit()
    else:
        print("O banco de dados já está populado. Nenhuma ação necessária.")

seed()

@app.get("/status")
def root():
    return {"Service available"}

@app.get("/extract")
def extract():
    elements = GeckoService.extract()
    processedData = GeckoService.processDate(elements)

    for item in processedData:
        #Categoria
        price_category = item.get('price_category')
        # Cripto
        symbol = item.get('symbol')
        name = item.get('name')
        rank = item.get('market_cap_rank')
        # Preço
        str_date =  item.get('last_updated')
        date= dt.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        current_price = item.get('current_price')

        category = session.query(CategoriaMercado).filter(CategoriaMercado.descricao == price_category).first()
        cripto = session.query(DimCripto).filter(DimCripto.simbolo == symbol).first()
        
        if cripto is None:
            cripto = DimCripto(name, symbol, rank, category.id)
            session.add(cripto)
            session.commit()
            
        fato = FatoCripto(cripto.id, date, current_price, price_category, category.id)

        session.add(fato)
        session.commit()

    return "Extração concluida com sucesso."

@app.get("/criptos/prices")
def get_fato_cripto():
    fatos = session.query(FatoCripto).order_by(FatoCripto.idCripto).all()
    return fatos

if __name__ == "__main__":
    uvicorn.run(app, port=8000)