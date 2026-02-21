import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.app import app
from src.db import prisma

@pytest_asyncio.fixture(scope="function")
async def prisma_client():
    if not prisma.is_connected():
        await prisma.connect()
    yield prisma
    await prisma.disconnect()

@pytest_asyncio.fixture(scope="function")
async def async_client(prisma_client):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client