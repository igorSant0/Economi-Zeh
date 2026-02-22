from prisma import Prisma
from src.lib.security.hash import hash_password


async def userSeed(prisma: Prisma):
    print("⏳ Seeding users...")

    users_data = [
        {
            "id_user": "user-uuid-1",
            "user_name": "Admin",
            "user_email": "admin@economizeh.com",
            "user_cpf": "00000000000",
            "user_password": "senha_admin_123",
        },
        {
            "id_user": "user-uuid-2",
            "user_name": "Igor Santana",
            "user_email": "igor@economizeh.com",
            "user_cpf": "11111111111",
            "user_password": "senha_igor_123",
        },
        {
            "id_user": "user-uuid-3",
            "user_name": "Hugao Monteiro",
            "user_email": "hugao@economizeh.com",
            "user_cpf": "22222222222",
            "user_password": "senha_hugao_123",
        },
    ]

    created_users = []

    for user_data in users_data:
        _hashed_password = await hash_password(user_data["user_password"])
        user = await prisma.user.upsert(
            where={"user_cpf": user_data["user_cpf"]},
            data={
                "create": {
                    "id_user": user_data["id_user"],
                    "user_name": user_data["user_name"],
                    "user_email": user_data["user_email"],
                    "user_cpf": user_data["user_cpf"],
                    "user_password": _hashed_password,
                },
                "update": {},
            },
        )
        created_users.append(user)

    return created_users
