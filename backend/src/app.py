from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.db import prisma
from src.lib.utils.apiError import ApiError
from src.routes.private.user_routes import router as user_router
from src.routes.private.login_routes import router as login_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Conectando ao Banco de Dados...")
    await prisma.connect()
    yield
    print("🛑 Desconectando do Banco de Dados...")
    await prisma.disconnect()


app = FastAPI(title="Economi-Zeh API", lifespan=lifespan)


app.include_router(user_router)
app.include_router(login_router)


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.message, "stack": exc.stack}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "API Economi-Zeh rodando com Prisma! 🚀"}
