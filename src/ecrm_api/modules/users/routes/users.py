from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from ecrm_api.core.auth_bearer import JWTBearer
from ecrm_api.modules.users.presenters.users import Users
from typing import List
from ecrm_api.core.persistence.db import get_db
from ecrm_api.core.presenters import BaseResult
from ecrm_api.modules.users.presenters.users import UserCreate, ListUserResult

users_router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
)

@users_router.post(
    "/",
    response_model=BaseResult,
    summary="Crear un nuevo usuario",
    dependencies=[Depends(JWTBearer())],
)
async def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db)) -> dict:
    return {"success": True, "detail": "Usuario creado con éxito"}


@users_router.get(
    "/",
    response_model=ListUserResult,
    summary="Obtener todos los usuarios",
    dependencies=[Depends(JWTBearer())],
)
async def get_user(request: Request, page: int = 1, per_page: int = 6, search: str = "", db: Session = Depends(get_db)) -> dict:
    return {"success": True, "data": {}}


@users_router.put(
    "/{id}",
    response_model=BaseResult,
    summary="Actualizar un usuario",
    dependencies=[Depends(JWTBearer())],
)
async def update_user(request: Request, id: str, db: Session = Depends(get_db)) -> dict:
    return {"success": True, "data": {}}


@users_router.delete(
    "/{id}",
    response_model=BaseResult,
    summary="Eliminar un usuario",
    dependencies=[Depends(JWTBearer())],
)
async def delete_user(request: Request, id: str, db: Session = Depends(get_db)) -> dict:
    return {"success": True, "data": {}}


@users_router.get(
    "/{id}",
    response_model=ListUserResult,
    summary="Obtener un usuario por su ID",
    dependencies=[Depends(JWTBearer())],
)
async def get_user(request: Request, id: str, db: Session = Depends(get_db)) -> dict:
    return {"success": True, "data": {}}
