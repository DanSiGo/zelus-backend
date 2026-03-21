from fastapi import FastAPI
from src.routes import items, report, user
from src.database import engine, Base

app = FastAPI(title="Zelus API")


print("--- Verificando Banco de Dados ---", flush=True)
try:
    # Força a criação das tabelas
    Base.metadata.create_all(bind=engine)
    print("Tabelas verificadas/criadas com sucesso!", flush=True)
except Exception as e:
    print(f"Erro ao conectar no banco: {e}", flush=True)



app.include_router(items.router)
app.include_router(report.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}