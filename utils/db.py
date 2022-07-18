from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgres_url = "postgresql://franciscodelgado_usuario_prueba:prueba_banco_198@postgresql-franciscodelgado.alwaysdata.net:5432/franciscodelgado_db_prueba"

engine = create_engine(postgres_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
