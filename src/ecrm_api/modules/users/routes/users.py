from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from ecrm_api.core.auth_bearer import JWTBearer
from ecrm_api.modules.users.presenters.users import Users
from typing import List
from ecrm_api.core.persistence.db import get_db, get_ext_db
from ecrm_api.core.presenters import BaseResult, ObjectResult

from ecrm_api.core.functions_jwt import get_user_current

from ecrm_api.modules.users.presenters.users import (
    UserCreate,
    UserUpdate,
    ChangePasswordSchema,
)

from ecrm_api.modules.users.services.users import (
    new,
    get_all,
    delete,
    update,
    get_one_by_id,
    change_password,
)

users_router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
)


@users_router.get(
    "/",
    response_model=ObjectResult,
    summary="Obtener todos los usuarios",
    dependencies=[Depends(get_user_current)],
)
async def get_user(
    request: Request,
    page: int = 1,
    per_page: int = 6,
    search: str = "",
    db: Session = Depends(get_db)
):
    return get_all(
        request=request, page=page, per_page=per_page, criteria_value=search, db=db)


@users_router.get(
    "/{id}",
    response_model=BaseResult,
    summary="Obtener un usuario por su ID",
    dependencies=[Depends(get_user_current)],
)
async def get_user(request: Request, id: str, db: Session = Depends(get_db)):
    return get_one_by_id(request=request, user_id=id, db=db)


@users_router.post(
    "/",
    response_model=BaseResult,
    summary="Crear un nuevo usuario",
    dependencies=[Depends(get_user_current)],
)
async def create_user(
    request: Request, user: UserCreate, db: Session = Depends(get_db)
):
    return new(request=request, user=user, db=db)


@users_router.put(
    "/{id}",
    response_model=BaseResult,
    summary="Actualizar un usuario",
    dependencies=[Depends(get_user_current)],
)
async def update_user(
    request: Request, id: str, user: UserUpdate, db: Session = Depends(get_db)
):
    return update(request=request, user_id=id, user=user, db=db)


@users_router.delete(
    "/{id}",
    response_model=BaseResult,
    summary="Eliminar un usuario",
    dependencies=[Depends(get_user_current)],
)
async def delete_user(request: Request, id: str, db: Session = Depends(get_db)):
    return delete(request=request, user_id=id, db=db)


# @users_router.post("/password", response_model=BaseResult, summary="Change password to a user.", dependencies=[Depends(JWTBearer())])
@users_router.post(
    "/password", response_model=BaseResult, summary="Change password to a user."
)
def reset_password(
    request: Request, password: ChangePasswordSchema, db: Session = Depends(get_db)
):
    return change_password(request=request, db=db, password=password)
