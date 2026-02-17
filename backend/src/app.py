from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.db import db
from src.lib.utils.apiError import ApiError


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


# Handler GLobal para ApiError
@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.message, "stack": exc.stack}
    )


# Rota de Teste Básica
@app.get("/")
def read_root():
    return {"message": "API Economi-Zeh rodando com Prisma! 🚀"}
