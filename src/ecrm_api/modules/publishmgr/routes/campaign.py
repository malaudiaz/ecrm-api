from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from ecrm_api.core.auth_bearer import JWTBearer
from typing import List
from ecrm_api.core.persistence.db import get_db, get_ext_db
from ecrm_api.core.presenters import BaseResult, ObjectResult

from ecrm_api.core.functions_jwt import get_user_current

from ecrm_api.modules.publishmgr.presenters.campaign import PublishCampaignBase

from ecrm_api.modules.publishmgr.services.campaign import (
    new,
    get_all,
    delete,
    update,
    get_one)

publishcampaign_router = APIRouter(
    prefix="/publishcampaign",
    tags=["Publicidad - Campañas"],
)


@publishcampaign_router.get(
    "/",
    response_model=ObjectResult,
    summary="Obtener todas las campañas",
    dependencies=[Depends(get_user_current)],
)
async def get_campaigns(
    request: Request,
    query: str = "",
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    return get_all(
        request=request, query=query, page=page, per_page=per_page, db=db)

@publishcampaign_router.get(
    "/{id}",
    response_model=BaseResult,
    summary="Obtener una Campaña por su ID",
    dependencies=[Depends(get_user_current)],
)
async def get_campaign(request: Request, id: str, db: Session = Depends(get_db)):
    return get_one(request=request, eid=id, db=db)


@publishcampaign_router.post(
    "/",
    response_model=BaseResult,
    summary="Crear una nueva campaña",
    dependencies=[Depends(get_user_current)],
)
async def create_campaign(
    request: Request, publishcampaign: PublishCampaignBase, db: Session = Depends(get_db)
):
    return new(request=request, publishcampaign=publishcampaign, db=db)


@publishcampaign_router.put(
    "/{id}",
    response_model=BaseResult,
    summary="Actualizar una campaña",
    dependencies=[Depends(get_user_current)],
)
async def update_campaign(
    request: Request, id: str, publishcampaign: PublishCampaignBase, db: Session = Depends(get_db)
):
    return update(request=request, eid=id, publishcampaign=publishcampaign, db=db)


@publishcampaign_router.delete(
    "/{id}",
    response_model=BaseResult,
    summary="Eliminar o cerrar una campaña",
    dependencies=[Depends(get_user_current)],
)
async def delete_campaign(request: Request, id: str, db: Session = Depends(get_db)):
    return delete(request=request, eid=id, db=db)

