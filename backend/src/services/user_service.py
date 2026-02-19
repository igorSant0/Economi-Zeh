from typing import Optional, TypedDict
from prisma.models import user as UserModel
from src.db import prisma
from src.lib.security.hash import hash_password
from src.lib.utils.apiError import ApiError
from src.lib.utils.prismaTools import find_many_with_page_info, update_parcial_data
from src.schemas.user_schema import (
    UserCreateData,
    UserParams,
    UserQuerys,
    UserUpdateData,
)


class ValidateDataDict(TypedDict, total=False):
    user_cpf: Optional[str]
    user_id: Optional[str]


class UserService:
    async def create(self, data: UserCreateData) -> UserModel:
        if await self.__validateIfExist({"user_cpf": data.cpf}):
            raise ApiError(status="CONFLICT", message="User already exist")

        _hashed_password = await hash_password(data.password)

        return await prisma.user.create(
            data={
                "user_name": data.name,
                "user_email": data.email,
                "user_cpf": data.cpf,
                "user_password": _hashed_password,
            }
        )

    async def getOne(self, params: UserParams) -> UserModel:
        _user = await self.__validateIfExist({"user_id": params.id_user})
        if _user is None:
            raise ApiError(status="NOT_FOUND", message="User not found")
        return _user

    async def getMany(self, filters: UserQuerys):
        where_clause = {}

        if filters.name:
            where_clause["user_name"] = {
                "contains": filters.name,
                "mode": "insensitive",
            }
        if filters.email:
            where_clause["user_email"] = filters.email
        if filters.cpf:
            where_clause["user_cpf"] = filters.cpf

        return await find_many_with_page_info(
            prisma.user,
            where=where_clause,
            page=filters.page or 1,
            limit=filters.limit or 10,
            order={"created_at": "desc"},
        )

    async def update(self, params: UserParams, data: UserUpdateData) -> UserModel:
        if await self.__validateIfExist({"user_id": params.id_user}) is None:
            raise ApiError(status="NOT_FOUND", message="User not found")

        _updated_data = await update_parcial_data(
            prisma.user,
            where={"id_user": params.id_user},
            data=data.model_dump(exclude_unset=True),
        )

        if _updated_data is None:
            raise ApiError(status="BAD_REQUEST", message="Need at least one field to update")

        return _updated_data

    async def delete(self, params: UserParams):
        if await self.__validateIfExist({"user_id": params.id_user}) is None:
            raise ApiError(status="NOT_FOUND", message="User not found")

        await prisma.user.update(where={"id_user": params.id_user}, data={"is_deleted": True})

    async def __validateIfExist(self, data: ValidateDataDict):
        user_cpf = data.get("user_cpf")
        id_user = data.get("user_id")
        if user_cpf:
            return await prisma.user.find_first(where={"user_cpf": user_cpf, "is_deleted": False})
        if id_user:
            return await prisma.user.find_first(where={"id_user": id_user, "is_deleted": False})
        return None
