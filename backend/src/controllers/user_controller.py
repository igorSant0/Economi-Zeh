from fastapi import status
from fastapi.responses import JSONResponse
from src.schemas.user_schema import UserCreateData, UserParams, UserQuerys, UserUpdateData
from src.services.user_service import UserService


class UserController:
    async def create(self, data: UserCreateData):
        user = await UserService().create(data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())

    async def getOne(self, params: UserParams):
        user = await UserService().getOne(params)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())

    async def getMany(self, filters: UserQuerys):
        users = await UserService().getMany(filters)
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)

    async def update(self, params: UserParams, data: UserUpdateData):
        user = await UserService().update(params, data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())

    async def delete(self, params: UserParams):
        await UserService().delete(params)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
