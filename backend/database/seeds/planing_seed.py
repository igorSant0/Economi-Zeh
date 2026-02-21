from datetime import datetime, timezone
from prisma import Prisma


async def planningSeed(prisma: Prisma):
    print("⏳ Seeding plannings...")

    plannings_data = [
        {
            "id_planning": "plan-uuid-1",
            "planning_reference_month": datetime(2026, 3, 1, tzinfo=timezone.utc),
            "planning_target_value": 1500.00,
            "planning_title": "Reserva de Emergência",
            "planning_description": "Guardar para o futuro",
            "planning_type": "SAVINGS",
            "fk_id_user": "user-uuid-2",
        },
        {
            "id_planning": "plan-uuid-2",
            "planning_reference_month": datetime(2026, 3, 1, tzinfo=timezone.utc),
            "planning_target_value": 500.00,
            "planning_title": "Orçamento de Lazer",
            "planning_description": "Limite para gastos com saídas",
            "planning_type": "BUDGET",
            "fk_id_user": "user-uuid-3",
        },
    ]

    for data in plannings_data:
        await prisma.planning.upsert(
            where={"id_planning": data["id_planning"]},
            data={
                "create": {
                    "id_planning": data["id_planning"],
                    "planning_reference_month": data["planning_reference_month"],
                    "planning_target_value": data["planning_target_value"],
                    "planning_title": data["planning_title"],
                    "planning_description": data["planning_description"],
                    "planning_type": data["planning_type"],
                    "fk_id_user": data["fk_id_user"],
                },
                "update": {
                    "planning_reference_month": data["planning_reference_month"],
                    "planning_target_value": data["planning_target_value"],
                    "planning_title": data["planning_title"],
                    "planning_description": data["planning_description"],
                    "planning_type": data["planning_type"],
                    # NÃO inclua "fk_id_user" aqui!
                },
            },
        )
