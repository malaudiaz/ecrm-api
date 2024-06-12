from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from ecrm_api.core.auth_bearer import JWTBearer
from typing import List
from ecrm_api.core.persistence.db import get_db
from ecrm_api.core.presenters import BaseResult, ObjectResult

from ecrm_api.modules.accountingentry.presenters.accrelopecategories import AccountingRelOperationsCategoriesBase
from ecrm_api.modules.accountingentry.services.accrelopecategories import get_all, new, delete

accountingentry_router = APIRouter(
    prefix="/accountingentry",
    tags=["Comprobante Contable"],
    # dependencies=[Depends(JWTBearer())]
)

@accountingentry_router.get("/", response_model=ObjectResult, summary="Obtener las catgorias por Tipos de Operación")
async def get_operation_type_with_categories(
    request: Request, page: int = 1, per_page: int = 6, search: str = "", db: Session = Depends(get_db)):
    return get_all(request=request, page=page, per_page=per_page, criteria_value=search, db=db)


@accountingentry_router.post("/", response_model=ObjectResult, summary="Crear nueva categoria por tipo de operación")
async def create_operation_type_with_categories(request: Request, opecategory: AccountingRelOperationsCategoriesBase, db: Session = Depends(get_db)):
    return new(request=request, opecategory=opecategory, db=db)

@accountingentry_router.delete("/{operation_type},{operation_category_name}", response_model=ObjectResult, 
                               summary="Eliminar categoria a un tipo de Operación")
async def delete_operation_with_categories(request: Request, operation_type: str, operation_category_name:str, db: Session = Depends(get_db)):
    return delete(request=request, operation_type=operation_type, operation_category_name=operation_category_name, db=db)

