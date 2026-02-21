import asyncio
import os
import sys
from seeds.category_expense_seed import categoryExpenseSeed
from seeds.category_seed import categorySeed
from seeds.expense_seed import expenseSeed
from seeds.planing_seed import planningSeed
from seeds.user_seed import userSeed
from src.db import prisma

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def main():
    print("🚀 Iniciando população do banco de dados...")

    await prisma.connect()

    try:
        await userSeed(prisma)

        await categorySeed(prisma)
        await planningSeed(prisma)
        await expenseSeed(prisma)

        await categoryExpenseSeed(prisma)

        print("🎉 Todas as seeds foram executadas com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao rodar seeds: {e}")

    finally:
        await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
