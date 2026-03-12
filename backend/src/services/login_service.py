from src.db import prisma
from src.schemas.login_schema import LoginData
from src.lib.utils.apiError import ApiError
from src.lib.security.jwt import create_access_token
from src.lib.security.hash import verify_password

class LoginService:
    async def login(self, data: LoginData):
        _user = await self.__validateIfExist(data)
        if _user is None:
            raise ApiError(status="NOT_FOUND", message="User not found")
        
        is_password_valid = await verify_password(data.user_password, _user.user_password)
        if not is_password_valid:
            raise ApiError(status="UNAUTHORIZED", message="Invalid password")
        
        if data.user_email:
            payload = {
            "user_id": _user.id_user,
            "user_email": _user.user_email,
        }
            
        if data.user_phone:
            payload = {
            "user_id": _user.id_user,
            "user_phone": _user.user_phone,
        }
        
        token = create_access_token(payload)
        return {"access_token": token, "token_type": "bearer"}



    async def __validateIfExist(self, data: LoginData):
        user_email = data.user_email
        user_phone = data.user_phone

        if user_email:
            return await prisma.user.find_first(where={"user_email": user_email, "is_deleted": False})
        if user_phone:
            return await prisma.user.find_first(where={"user_phone": user_phone, "is_deleted": False})
        

        