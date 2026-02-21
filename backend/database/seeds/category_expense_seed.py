from prisma import Prisma


async def categoryExpenseSeed(prisma: Prisma):
    print("⏳ Seeding category_expense relations...")

    relations_data = [
        {
            "fk_id_expense": "exp-uuid-1",
            "fk_id_category": "cat-uuid-1",
        },
        {
            "fk_id_expense": "exp-uuid-2",
            "fk_id_category": "cat-uuid-2",
        },
    ]

    for data in relations_data:
        exists = await prisma.category_expense.find_unique(
            where={
                "fk_id_expense_fk_id_category": {
                    "fk_id_expense": data["fk_id_expense"],
                    "fk_id_category": data["fk_id_category"],
                }
            }
        )

        if not exists:
            await prisma.category_expense.create(
                data={
                    "fk_id_expense": data["fk_id_expense"],
                    "fk_id_category": data["fk_id_category"],
                }
            )
