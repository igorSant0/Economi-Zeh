from src.schemas.login_schema import LoginData
from src.services.login_service import LoginService

class LoginController:
    def __init__(self):
        self.service = LoginService()

    async def login(self, data: LoginData):
        return await self.service.login(data)