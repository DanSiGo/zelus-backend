from fastapi import FastAPI
from src.routes import items

app = FastAPI(title="Zelus API")

app.include_router(items.router)

@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}