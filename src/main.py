from fastapi import FastAPI
from src.routes import items
from src.database import engine, Base
import src.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zelus API")

app.include_router(items.router)

@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}