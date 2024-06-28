
"""coding=utf-8."""
 
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from ecrm_api.core.presenters import ObjectResult

class PublishDepartamentBase(BaseModel):
    code: str
    name: str
    comercial_group_eid: Optional[str]
    store_code_legal: Optional[str]
    store_code_natural: Optional[str]
       
    @field_validator('code')
    def code_not_empty(cls, code):
        if not code:
            raise ValueError('Código de departamento es requerid')
        return code  
    
    @field_validator('name')
    def name_not_empty(cls, name):
        if not name:
            raise ValueError('Nombre de departamento es requerido')
        return name  
    
class PublishDepartamentSchema(PublishDepartamentBase):
    
    is_active: bool = True
    
    class Config:
        orm_mode = True 
        
