from fastapi import FastAPI
from src.routes import auth, report, user 
from src.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Zelus API")

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Erro ao conectar no banco: {e}", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(report.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}