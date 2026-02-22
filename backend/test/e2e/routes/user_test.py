import pytest
from httpx import AsyncClient
from dirty_equals import IsStr, IsUUID, IsDatetime, IsList

from database.seeds.user_seed import userSeed

pytestmark = pytest.mark.asyncio

USER_ROUTE = "/user"
UNEXIST_ID = "invalid-id-1234"

new_user_data = {
    "user_name": "Sophia Monteiro",
    "user_email": "sophia.monteiro@testemail.com",
    "user_cpf": "12345678901",
    "user_password": "secure_password",
}

expect_get_one_body = {
    "id_user": IsUUID() | IsStr(),
    "user_name": IsStr(),
    "user_email": IsStr(),
    "user_cpf": IsStr(),
    "created_at": IsDatetime() | IsStr(),
}

expect_get_many_body = expect_get_one_body


class TestCreate:

    async def test_should_create_user_successfully(self, async_client: AsyncClient):
        res = await async_client.post(USER_ROUTE, json=new_user_data)

        assert res.status_code == 201
        print(res.json())
        assert res.json() == expect_get_one_body

    async def test_should_return_409_when_cpf_already_exists(self, async_client: AsyncClient):
        await async_client.post(USER_ROUTE, json=new_user_data)

        duplicate_payload = {**new_user_data, "user_email": "outro@email.com"}
        res = await async_client.post(USER_ROUTE, json=duplicate_payload)

        assert res.status_code == 409
        assert "already exist" in res.json()["error"].lower()

class TestGetOne:

    async def test_should_get_one_user_successfully(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        res = await async_client.get(f"{USER_ROUTE}/{user.id_user}")

        assert res.status_code == 200
        assert res.json() == expect_get_one_body

    async def test_should_return_not_found_with_invalid_id(self, async_client: AsyncClient):
        res = await async_client.get(f"{USER_ROUTE}/{UNEXIST_ID}")

        assert res.status_code == 404
        assert res.json()["error"] == "User not found"

class TestGetMany:

    async def test_should_get_many_users_successfully(self, async_client: AsyncClient):
        res = await async_client.get(USER_ROUTE)

        assert res.status_code == 200
        
        response_data = res.json()
        assert "data" in response_data
        assert "pagination" in response_data
        assert isinstance(response_data["data"], list)
        assert len(response_data["data"]) >= 1

        for item in response_data["data"]:
            assert item == expect_get_many_body

class TestUpdate:

    async def test_should_update_user_successfully(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        update_payload = {"user_name": "updated_name"}
        res = await async_client.put(f"{USER_ROUTE}/{user.id_user}", json=update_payload)

        assert res.status_code == 200

        expected_updated_body = {**expect_get_one_body, "user_name": "updated_name"}
        assert res.json() == expected_updated_body

class TestDelete:

    async def test_should_delete_user_successfully(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        res = await async_client.delete(f"{USER_ROUTE}/{user.id_user}")
        assert res.status_code == 204

        get_res = await async_client.get(f"{USER_ROUTE}/{user.id_user}")
        assert get_res.status_code == 404