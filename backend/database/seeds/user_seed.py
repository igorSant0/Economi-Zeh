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
            "user_phone": "999999999",
            "user_password": "admin_123",
        },
        {
            "id_user": "user-uuid-2",
            "user_name": "Igor Santana",
            "user_email": "igor@economizeh.com",
            "user_cpf": "11111111111",
            "user_phone": "888888888",
            "user_password": "igor_123",
        },
        {
            "id_user": "user-uuid-3",
            "user_name": "Hugao Monteiro",
            "user_email": "hugao@economizeh.com",
            "user_cpf": "22222222222",
            "user_phone": "777777777",
            "user_password": "hugao_123",
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
                    "user_phone": user_data["user_phone"],
                    "user_password": _hashed_password,
                },
                "update": {},
            },
        )
        created_users.append(user)

    return created_users
