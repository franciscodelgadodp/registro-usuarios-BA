import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

database_name = os.getenv("DATABASE_NAME")
database_pwd = os.getenv("DATABASE_PWD")

postgres_url = f"postgresql://{database_name}:{database_pwd}@postgresql-franciscodelgado.alwaysdata.net:5432/franciscodelgado_db_prueba"

engine = create_engine(postgres_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
