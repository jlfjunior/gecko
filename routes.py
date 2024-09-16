from fastapi import APIRouter
import datetime as dt
from sqlalchemy.orm import joinedload
from services.database import get_session, seed_database
from services.geckoService import GeckoService
from models.fatoCripto import FatoCripto
from models.categoriaMercado import CategoriaMercado
from models.dimCripto import DimCripto

router = APIRouter()

seed_database()
session = get_session()

@router.get("/status")
def root():
    return {"Service available"}

@router.post("/extract")
def extract():
    elements = GeckoService.extract()
    processedData = GeckoService.processDate(elements)

    for item in processedData:
        price_category = item.get('price_category')
        symbol = item.get('symbol')
        name = item.get('name')
        rank = item.get('market_cap_rank')
        str_date = item.get('last_updated')
        date = dt.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ')
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

    return "Extração concluída com sucesso."

@router.get("/criptos/prices")
def get_fato_cripto(simbolo: str = None):
    query = session.query(FatoCripto).join(DimCripto).order_by(FatoCripto.idCripto)

    if simbolo:
        query = query.filter(DimCripto.simbolo == simbolo)

    fatos = query.all()

    response = []

    for fato in fatos:
        response.append({
            "id": fato.id,
            "idCripto": fato.idCripto,
            "data": fato.data,
            "preco_atual": fato.preco_atual,
            "categoria_preco": fato.categoria_preco
        })

    return response

@router.get("/criptos")
def get_criptos(simbolo: str = None):
    query = session.query(DimCripto).options(joinedload(DimCripto.categoria))

    if simbolo:
        query = query.filter(DimCripto.simbolo == simbolo)

    criptos = query.all()
    response = []

    for cripto in criptos:
        response.append({
            "id": cripto.id,
            "nome": cripto.nome,
            "simbolo": cripto.simbolo,
            "rank": cripto.rank,
            "categoria": {
                "id": cripto.categoria.id,
                "descricao": cripto.categoria.descricao
            }
        })

    return response