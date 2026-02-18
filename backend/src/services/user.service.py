from prisma.models import user as UserModel # O modelo agora é minúsculo
from src.db import db
from src.schema.user.schema import UserCreate, UserGetMany, UserUpdate, UserDelete
from src.lib.security.hash import hash_password
from src.lib.utils.apiError import ApiError

class UserService:
    async def create(self, data: UserCreate) -> UserModel:
        # 1. Validação de Email (campo user_email)
        if await db.user.find_unique(where={"user_cpf": data.cpf}):
            raise ApiError(status=400, message="Email already in use")
        
        # 2. Segurança
        hashed_password = hash_password(data.password)

        # 3. Mapeamento Manual (Adapter)
        # Pydantic (name) -> Prisma (user_name)
        return await db.user.create(
            data={
                "user_name": data.name,
                "user_email": data.email,
                "user_cpf": data.cpf,
                "user_password": hashed_password,
                # created_at é automático pelo @default(now())
            }
        )

    async def get_many(self, filters: UserGetMany) -> list[UserModel]:
        where_clause = {}

        # Note a redundância: "user_name"
        if filters.name:
            where_clause["user_name"] = {"contains": filters.name, "mode": "insensitive"}
        
        if filters.email:
            where_clause["user_email"] = filters.email
            
        if filters.cpf:
            where_clause["user_cpf"] = filters.cpf

        skip = (filters.page - 1) * filters.limit

        return await db.user.find_many(
            where=where_clause,
            skip=skip,
            take=filters.limit,
            order={"created_at": "desc"}
        )

    async def update(self, id_user: str, data: UserUpdate) -> UserModel | None:
        user = await db.user.find_unique(where={"id_user": id_user})
        if not user:
            return None

        # Pega os dados limpos do Pydantic (ex: {'name': 'Igor'})
        raw_data = data.model_dump(exclude_unset=True)
        prisma_data = {}

        # Tradução manual campo a campo
        if "name" in raw_data:
            prisma_data["user_name"] = raw_data["name"]
        if "email" in raw_data:
            prisma_data["user_email"] = raw_data["email"]
        if "cpf" in raw_data:
            prisma_data["user_cpf"] = raw_data["cpf"]

        return await db.user.update(
            where={"id_user": id_user},
            data=prisma_data
        )

    async def delete(self, data: UserDelete) -> UserModel | None:
        where_clause = {"id_user": data.id_user}
        
        if data.cpf:
            where_clause["user_cpf"] = data.cpf

        # Verifica existência
        if not await db.user.find_unique(where=where_clause):
            return None

        return await db.user.delete(where={"id_user": data.id_user})