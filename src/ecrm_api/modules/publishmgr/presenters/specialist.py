
"""coding=utf-8."""
 
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List

class PublishSpecialistBase(BaseModel):
    code: str
    user_name: str
    publish_departament_eid: str
       
    @field_validator('code')
    def code_not_empty(cls, code):
        if not code:
            raise ValueError('Código de especialista es requerid')
        return code  
    
    @field_validator('user_name')
    def user_name_not_empty(cls, user_name):
        if not user_name:
            raise ValueError('Nombre de usuario es requerido')
        return user_name  
    
class PublishSpecialistSchema(PublishSpecialistBase):
    
    is_active: bool = True
    
    class Config:
        orm_mode = True 