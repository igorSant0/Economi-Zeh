import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app
from src.db import prisma

@pytest_asyncio.fixture(scope="session")
async def async_client():

    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="session")
async def prisma_client():

    return prisma