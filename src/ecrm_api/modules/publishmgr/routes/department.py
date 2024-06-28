from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from ecrm_api.core.auth_bearer import JWTBearer
from typing import List
from ecrm_api.core.persistence.db import get_db, get_ext_db
from ecrm_api.core.presenters import BaseResult

from ecrm_api.core.functions_jwt import get_user_current

from ecrm_api.modules.publishmgr.presenters.departament import PublishDepartamentBase

from ecrm_api.modules.publishmgr.services.departament import (
    new,
    get_all,
    delete,
    update,
    get_one)

publishdepartment_router = APIRouter(
    prefix="/publishdepartament",
    tags=["Publicidad - Departamentos"],
)


@publishdepartment_router.get(
    "/",
    response_model=BaseResult,
    summary="Obtener todos los departamentos",
    dependencies=[Depends(get_user_current)],
)
async def get_departments(
    request: Request,
    page: int = 1,
    per_page: int = 6,
    search: str = "",
    db: Session = Depends(get_db)
):
    return get_all(
        request=request, page=page, per_page=per_page, criteria_value=search, db=db)


@publishdepartment_router.get(
    "/{id}",
    response_model=BaseResult,
    summary="Obtener un Departamento por su ID",
    dependencies=[Depends(get_user_current)],
)
async def get_departament(request: Request, id: str, db: Session = Depends(get_db)):
    return get_one(request=request, eid=id, db=db)


@publishdepartment_router.post(
    "/",
    response_model=BaseResult,
    summary="Crear un nuevo departemento",
    dependencies=[Depends(get_user_current)],
)
async def create_department(
    request: Request, publishdepartament: PublishDepartamentBase, db: Session = Depends(get_db)
):
    return new(request=request, publishdepartament=publishdepartament, db=db)


@publishdepartment_router.put(
    "/{id}",
    response_model=BaseResult,
    summary="Actualizar un departamento",
    dependencies=[Depends(get_user_current)],
)
async def update_departament(
    request: Request, id: str, publishdepartament: PublishDepartamentBase, db: Session = Depends(get_db)
):
    return update(request=request, eid=id, publishdepartament=publishdepartament, db=db)


@publishdepartment_router.delete(
    "/{id}",
    response_model=BaseResult,
    summary="Eliminar un departamento",
    dependencies=[Depends(get_user_current)],
)
async def delete_departament(request: Request, id: str, db: Session = Depends(get_db)):
    return delete(request=request, eid=id, db=db)

