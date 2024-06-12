
"""coding=utf-8."""
 
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from ecrm_api.core.presenters import ObjectResult

class AccountingRelOperationsCategoriesBase(BaseModel):
    operation_type: Optional[str]
    operation_category_name: Optional[str]
        
    @field_validator('operation_type')
    def operation_type_not_empty(cls, operation_type):
        if not operation_type:
            raise ValueError('Tipo de Operacion requerida')
        return operation_type  
    
    @field_validator('operation_category_name')
    def operation_category_name_not_empty(cls, operation_category_name):
        if not operation_category_name:
            raise ValueError('Categoría de Operacion requerida')
        return operation_category_name  
