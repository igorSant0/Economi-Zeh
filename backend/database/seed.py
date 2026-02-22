import asyncio
import os
import sys
from .seeds.category_expense_seed import categoryExpenseSeed
from .seeds.category_seed import categorySeed
from .seeds.expense_seed import expenseSeed
from .seeds.planing_seed import planningSeed
from .seeds.user_seed import userSeed
from src.db import prisma

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

async def all_seeds(prisma_client):
    await userSeed(prisma_client)
    await categorySeed(prisma_client)
    await planningSeed(prisma_client)
    await expenseSeed(prisma_client)
    await categoryExpenseSeed(prisma_client)

async def main():
    print("🚀 Iniciando população do banco de dados...")

    await prisma.connect()

    try:
        await all_seeds(prisma)
        print("🎉 Todas as seeds foram executadas com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao rodar seeds: {e}")

    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    asyncio.run(main())