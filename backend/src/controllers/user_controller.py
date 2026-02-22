from src.schemas.user_schema import UserCreateData, UserParams, UserQuerys, UserUpdateData
from src.services.user_service import UserService


class UserController:
    def __init__(self):
        self.service = UserService()

    async def create(self, data: UserCreateData):
        return await self.service.create(data)

    async def getOne(self, params: UserParams):
        return await self.service.getOne(params)

    async def getMany(self, filters: UserQuerys):
        return await self.service.getMany(filters)

    async def update(self, params: UserParams, data: UserUpdateData):
        return await self.service.update(params, data)

    async def delete(self, params: UserParams):
        return await self.service.delete(params)
