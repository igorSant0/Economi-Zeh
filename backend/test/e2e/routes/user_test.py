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
        assert res.json() == expect_get_one_body

    async def test_should_return_409_when_cpf_already_exists(self, async_client: AsyncClient):
        await async_client.post(USER_ROUTE, json=new_user_data)

        duplicate_payload = {**new_user_data, "user_email": "outro@email.com"}
        res = await async_client.post(USER_ROUTE, json=duplicate_payload)

        assert res.status_code == 409
        assert "already exist" in res.json()["error"].lower()

    async def test_should_return_422_when_missing_required_fields(self, async_client: AsyncClient):
        incomplete_data = {"user_name": "Test User"}
        res = await async_client.post(USER_ROUTE, json=incomplete_data)

        assert res.status_code == 422

    async def test_should_return_422_when_email_is_invalid(self, async_client: AsyncClient):
        invalid_email_data = {**new_user_data, "user_email": "invalid-email"}
        res = await async_client.post(USER_ROUTE, json=invalid_email_data)

        assert res.status_code == 422

    async def test_should_return_422_when_password_is_too_short(self, async_client: AsyncClient):
        short_password_data = {**new_user_data, "user_email": "test@test.com", "user_password": "123"}
        res = await async_client.post(USER_ROUTE, json=short_password_data)

        assert res.status_code == 422

    async def test_should_return_422_when_cpf_is_invalid(self, async_client: AsyncClient):
        invalid_cpf_data = {**new_user_data, "user_email": "test@test.com", "user_cpf": "123"}
        res = await async_client.post(USER_ROUTE, json=invalid_cpf_data)

        assert res.status_code == 422

    async def test_should_return_422_when_name_is_too_short(self, async_client: AsyncClient):
        short_name_data = {**new_user_data, "user_email": "test@test.com", "user_name": "AB"}
        res = await async_client.post(USER_ROUTE, json=short_name_data)

        assert res.status_code == 422

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

    async def test_should_filter_users_by_name(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user_name = users[0].user_name

        res = await async_client.get(f"{USER_ROUTE}?user_name={user_name}")

        assert res.status_code == 200
        response_data = res.json()
        assert len(response_data["data"]) >= 1

    async def test_should_filter_users_by_email(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user_email = users[0].user_email

        res = await async_client.get(f"{USER_ROUTE}?user_email={user_email}")

        assert res.status_code == 200
        response_data = res.json()
        assert len(response_data["data"]) >= 1

    async def test_should_filter_users_by_cpf(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user_cpf = users[0].user_cpf

        res = await async_client.get(f"{USER_ROUTE}?user_cpf={user_cpf}")

        assert res.status_code == 200
        response_data = res.json()
        assert len(response_data["data"]) >= 1

    async def test_should_paginate_users(self, async_client: AsyncClient):
        res = await async_client.get(f"{USER_ROUTE}?page=1&limit=2")

        assert res.status_code == 200
        response_data = res.json()
        assert response_data["pagination"]["page"] == 1
        assert response_data["pagination"]["perPage"] == 2

    async def test_should_return_empty_list_when_no_users_match_filter(self, async_client: AsyncClient):
        res = await async_client.get(f"{USER_ROUTE}?user_name=NonExistentUser12345")

        assert res.status_code == 200
        response_data = res.json()
        assert len(response_data["data"]) == 0

class TestUpdate:

    async def test_should_update_user_successfully(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        update_payload = {"user_name": "updated_name"}
        res = await async_client.put(f"{USER_ROUTE}/{user.id_user}", json=update_payload)

        assert res.status_code == 200

        expected_updated_body = {**expect_get_one_body, "user_name": "updated_name"}
        assert res.json() == expected_updated_body

    async def test_should_return_404_when_updating_nonexistent_user(self, async_client: AsyncClient):
        update_payload = {"user_name": "updated_name"}
        res = await async_client.put(f"{USER_ROUTE}/{UNEXIST_ID}", json=update_payload)

        assert res.status_code == 404
        assert res.json()["error"] == "User not found"

    async def test_should_return_400_when_updating_without_fields(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        res = await async_client.put(f"{USER_ROUTE}/{user.id_user}", json={})

        assert res.status_code == 400
        assert "at least one field" in res.json()["error"].lower()

    async def test_should_return_422_when_updating_with_invalid_email(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        invalid_payload = {"user_email": "invalid-email"}
        res = await async_client.put(f"{USER_ROUTE}/{user.id_user}", json=invalid_payload)

        assert res.status_code == 422

class TestDelete:

    async def test_should_delete_user_successfully(self, async_client: AsyncClient, prisma_client):
        users = await userSeed(prisma_client)
        user = users[0]

        res = await async_client.delete(f"{USER_ROUTE}/{user.id_user}")
        assert res.status_code == 204

        get_res = await async_client.get(f"{USER_ROUTE}/{user.id_user}")
        assert get_res.status_code == 404

    async def test_should_return_404_when_deleting_nonexistent_user(self, async_client: AsyncClient):
        res = await async_client.delete(f"{USER_ROUTE}/{UNEXIST_ID}")

        assert res.status_code == 404
        assert res.json()["error"] == "User not found"