import pytest
from httpx import AsyncClient
from database.seeds.user_seed import userSeed

pytestmark = pytest.mark.asyncio

LOGIN_ROUTE = "/auth/login"

class TestLogin:
    async def test_should_login_user_successfully(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)

        correct_login_data = {
            "user_email": users[0].user_email,
            "user_password": "@ValidPassword123",
        }

        res = await async_client.post(LOGIN_ROUTE, json=correct_login_data)
        assert res.status_code == 200
        assert "access_token" in res.json()

    async def test_should_not_login_user_with_wrong_password(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)

        wrong_password_data = {
            "user_email": users[0].user_email,
            "user_password": "@WrongPassword123",
        }

        # TODO: aparentemente a api de erro não está retornando as mensagens colocadas
        res = await async_client.post(LOGIN_ROUTE, json=wrong_password_data)
        assert res.status_code == 401