from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db import db


# Configuração do Ciclo de Vida (Ligar/Desligar banco)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Conectando ao Banco de Dados...")
    await db.connect()
    yield
    print("🛑 Desconectando do Banco de Dados...")
    await db.disconnect()


# Inicializa o App com o lifespan
app = FastAPI(title="Economi-Zeh API", lifespan=lifespan)


# Rota de Teste Básica
@app.get("/")
def read_root():
    return {"message": "API Economi-Zeh rodando com Prisma! 🚀"}
