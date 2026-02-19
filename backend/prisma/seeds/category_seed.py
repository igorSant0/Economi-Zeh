from prisma import Prisma


async def categorySeed(prisma: Prisma):
    print("⏳ Seeding categories...")

    categories_data = [
        {
            "id_category": "cat-uuid-1",
            "category_title": "Alimentação",
            "category_color_hex": "#FF5733",
            "fk_id_user": "user-uuid-1",
        },
        {
            "id_category": "cat-uuid-2",
            "category_title": "Transporte",
            "category_color_hex": "#3357FF",
            "fk_id_user": "user-uuid-2",
        },
        {
            "id_category": "cat-uuid-3",
            "category_title": "Lazer",
            "category_color_hex": "#33FF57",
            "fk_id_user": "user-uuid-3",
        },
    ]

    for data in categories_data:
        await prisma.category.upsert(
            where={"id_category": data["id_category"]},
            data={
                "create": {
                    "id_category": data["id_category"],
                    "category_title": data["category_title"],
                    "category_color_hex": data["category_color_hex"],
                    "fk_id_user": data["fk_id_user"],
                },
                "update": {
                    "category_title": data["category_title"],
                    "category_color_hex": data["category_color_hex"],
                },
            },
        )
