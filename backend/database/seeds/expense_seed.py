from datetime import datetime, timezone
from prisma import Prisma


async def expenseSeed(prisma: Prisma):
    print("⏳ Seeding expenses...")

    expenses_data = [
        {
            "id_expense": "exp-uuid-1",
            "expense_description": "Almoço RU",
            "expense_unit_value": 1.50,
            "expense_quantity": 1.0,
            "expense_date": datetime.now(timezone.utc),
            "expense_total_value": 1.50,
            "fk_id_user": "user-uuid-2",
        },
        {
            "id_expense": "exp-uuid-2",
            "expense_description": "Uber para o Laboratório",
            "expense_unit_value": 15.00,
            "expense_quantity": 1.0,
            "expense_date": datetime.now(timezone.utc),
            "expense_total_value": 15.00,
            "fk_id_user": "user-uuid-3",
        },
    ]

    for data in expenses_data:
        await prisma.expense.upsert(
            where={"id_expense": data["id_expense"]},
            data={
                "create": {
                    "id_expense": data["id_expense"],
                    "expense_description": data["expense_description"],
                    "expense_unit_value": data["expense_unit_value"],
                    "expense_quantity": data["expense_quantity"],
                    "expense_date": data["expense_date"],
                    "expense_total_value": data["expense_total_value"],
                    "fk_id_user": data["fk_id_user"],
                },
                "update": {
                    "expense_description": data["expense_description"],
                    "expense_unit_value": data["expense_unit_value"],
                    "expense_quantity": data["expense_quantity"],
                    "expense_date": data["expense_date"],
                    "expense_total_value": data["expense_total_value"],
                },
            },
        )
