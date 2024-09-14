from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.mapping import Base
from models.categoriaMercado import CategoriaMercado

USER='root'
PASSWORD='gecko!23'
PORT=3306
DATABASE_NAME='Gecko'
DATABASE_URL = f'mysql+pymysql://{USER}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    return SessionLocal()

def seed_database():
    session = get_session()
    Base.metadata.create_all(bind=engine)

    exists = session.query(CategoriaMercado).count()

    if exists == 0:
        c1 = CategoriaMercado(1, "Low")
        c2 = CategoriaMercado(2, "Medium")  
        c3 = CategoriaMercado(3, "High")
        
        session.add_all([c1, c2, c3])
        session.commit()
    else:
        print("O banco de dados já está populado.")