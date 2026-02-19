from typing import List
from fastapi import APIRouter, Body, Depends
from src.config.routes_config import paths
from src.controllers.user_controller import UserController
from src.schemas.user_schema import (
    UserCreateData,
    UserParams,
    UserQuerys,
    UserResponse,
    UserUpdateData,
)

controller = UserController()
router = APIRouter(prefix=paths.user.PREFIX, tags=["User"])


@router.post("", response_model=UserResponse)
async def create_user(data: UserCreateData = Body(...)):
    return await controller.create(data)


@router.get("", response_model=List[UserResponse])
async def get_users(filters: UserQuerys = Depends()):
    return await controller.getMany(filters)


@router.get(paths.user.GET_BY_ID, response_model=UserResponse)
async def get_user(params: UserParams = Depends()):
    return await controller.getOne(params)


@router.put(paths.user.GET_BY_ID, response_model=UserResponse)
async def update_user(params: UserParams = Depends(), data: UserUpdateData = Body(...)):
    return await controller.update(params, data)


@router.delete(paths.user.GET_BY_ID)
async def delete_user(params: UserParams = Depends()):
    return await controller.delete(params)
