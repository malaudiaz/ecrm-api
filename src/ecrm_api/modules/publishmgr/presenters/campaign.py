
"""coding=utf-8."""
 
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List

class PublishCampaignBase(BaseModel):
    year: str
    name: str
       
    @field_validator('year')
    def year_not_empty(cls, year):
        if not year:
            raise ValueError('Año de campaña es requerid')
        return year  
    
    @field_validator('name')
    def name_not_empty(cls, name):
        if not name:
            raise ValueError('Nombre de campaña es requerido')
        return name  
    
class CampaignSchema(PublishCampaignBase):
    
    is_active: bool = True
    
    class Config:
        orm_mode = True 