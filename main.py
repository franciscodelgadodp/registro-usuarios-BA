from fastapi import FastAPI


from adapters import sql_alchemy_orm
from routers import user, authentication
from utils.db import engine

sql_alchemy_orm.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.router)
# app.include_router(product.router)
app.include_router(user.router)


@app.get("/")
def api_description():
    return {
        "descripcion": "API Banco Azteca",
        "creada_por": "Francisco Delgado"
    }
