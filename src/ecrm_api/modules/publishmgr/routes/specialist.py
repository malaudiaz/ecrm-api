from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from ecrm_api.core.auth_bearer import JWTBearer
from typing import List
from ecrm_api.core.persistence.db import get_db, get_ext_db
from ecrm_api.core.presenters import BaseResult, ObjectResult

from ecrm_api.core.functions_jwt import get_user_current

from ecrm_api.modules.publishmgr.presenters.specialist import PublishSpecialistBase

from ecrm_api.modules.publishmgr.services.specialist import (
    new,
    get_all,
    delete,
    update,
    get_one)

publishspecialist_router = APIRouter(
    prefix="/publishspecialist",
    tags=["Publicidad - Especialistas"],
)


@publishspecialist_router.get(
    "/",
    response_model=ObjectResult,
    summary="Obtener todos los especialistas",
    dependencies=[Depends(get_user_current)],
)
async def get_specialists(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    query: str = "",
    db: Session = Depends(get_db)
):
    return get_all(
        request=request, page=page, per_page=per_page, query=query, db=db)


@publishspecialist_router.get(
    "/{id}",
    response_model=BaseResult,
    summary="Obtener un Especialista por su ID",
    dependencies=[Depends(get_user_current)],
)
async def get_specialist(request: Request, id: str, db: Session = Depends(get_db)):
    return get_one(request=request, eid=id, db=db)


@publishspecialist_router.post(
    "/",
    response_model=BaseResult,
    summary="Crear un nuevo especialista",
    dependencies=[Depends(get_user_current)],
)
async def create_specialist(
    request: Request, publishspecialist: PublishSpecialistBase, db: Session = Depends(get_db)
):
    return new(request=request, publishspecialist=publishspecialist, db=db)


@publishspecialist_router.put(
    "/{id}",
    response_model=BaseResult,
    summary="Actualizar un Especialista",
    dependencies=[Depends(get_user_current)],
)
async def update_specialist(
    request: Request, id: str, publishspecialist: PublishSpecialistBase, db: Session = Depends(get_db)
):
    return update(request=request, eid=id, publishspecialist=publishspecialist, db=db)


@publishspecialist_router.delete(
    "/{id}",
    response_model=BaseResult,
    summary="Eliminar un es[ecia;ista]",
    dependencies=[Depends(get_user_current)],
)
async def delete_specialist(request: Request, id: str, db: Session = Depends(get_db)):
    return delete(request=request, eid=id, db=db)

