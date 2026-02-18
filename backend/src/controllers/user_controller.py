from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from src.services.user_service import *

class UserController:
    async def create(self, data: UserCreate):
        user = await UserService().create(data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())

    async def getOne(self, data: UserGetOne):
        user = await UserService().getOne(data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())

    async def getMany(self, filters: UserGetMany):
        users = await UserService().getMany(filters)
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)

    async def update(self, data: UserUpdate):
        user = await UserService().update(data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())
    
    async def delete(self, data: UserDelete):
        await UserService().delete(data)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)