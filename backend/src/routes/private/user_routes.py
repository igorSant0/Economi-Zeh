from fastapi import APIRouter, Depends
from src.controllers.user_controller import UserController
from src.schemas.user_schema import UserCreate, UserGetOne, UserGetMany, UserUpdate, UserDelete
from src.config.routes_config import paths

controller = UserController()
router = APIRouter(prefix=paths.user.PREFIX, tags=["User"])


@router.post("")
async def create_user(data: UserCreate):
    return await controller.create(data)


@router.get("")
async def get_users(filters: UserGetMany = Depends()):
    return await controller.getMany(filters)


@router.get(paths.user.GET_BY_ID)
async def get_user(data: UserGetOne = Depends()):
    return await controller.getOne(data)


@router.put(paths.user.GET_BY_ID)
async def update_user(data: UserUpdate):
    return await controller.update(data)


@router.delete(paths.user.GET_BY_ID)
async def delete_user(data: UserDelete):
    return await controller.delete(data)

