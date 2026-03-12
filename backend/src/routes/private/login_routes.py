from fastapi import APIRouter, Body
from src.config.routes_config import paths
from src.controllers.login_controller import LoginController
from src.schemas.login_schema import LoginData

login = LoginController()
router = APIRouter(prefix=paths.auth.PREFIX, tags=["Login"])

@router.post(paths.auth.LOGIN, status_code=200)
async def login_user(data: LoginData = Body(...)):
    return await login.login(data)