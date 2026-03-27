from fastapi import FastAPI
# 1. Adicionamos 'auth' aqui na lista de importação
from src.routes import auth, report, user 
from src.database import engine, Base

# --- INÍCIO DA MUDANÇA (ISSUE #5) ---
app = FastAPI(
    title="Zelus API 🏙️",
    description="""
**API oficial do aplicativo Zelus para zeladoria urbana.**

Aqui você pode interagir com o sistema para:
* 🔐 **Autenticação:** Fazer login e gerar tokens de segurança.
* 👤 **Usuários:** Criar contas e gerenciar acessos.
* 📝 **Denúncias:** Relatar problemas na cidade (buracos, postes quebrados, lixo, etc).

_Projeto desenvolvido pela equipe Unifor._
    """,
    version="1.0.0",
    contact={
        "name": "Equipe Zelus - Unifor",
        "url": "https://github.com/UniforGroupProjects/zelus-backend",
    }
)
# --- FIM DA MUDANÇA ---

print("--- Verificando Banco de Dados ---", flush=True)
try:
    # Força a criação das tabelas no banco de dados
    Base.metadata.create_all(bind=engine)
    print("Tabelas verificadas/criadas com sucesso!", flush=True)
except Exception as e:
    print(f"Erro ao conectar no banco: {e}", flush=True)

# 2. Registramos as rotas. A de auth (login) é bom ficar em primeiro!
app.include_router(auth.router)
app.include_router(report.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}