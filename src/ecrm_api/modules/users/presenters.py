"""coding=utf-8."""
 
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from ecrm_api.core.presenters import ObjectResult
 
class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    
    @field_validator('username')
    def username_not_empty(cls, username):
        if not username:
            raise ValueError('Nombre de usuario requerido')
        return username  

class UserCreate(UserBase):
    password: str 
    
    @field_validator('password')
    def password_not_empty(cls, password):
        if not password:
            raise ValueError('Contraseña Requerida')
        return password 

class UserShema(UserCreate):
    id: UUID
    is_active: bool
    
    class Config:
        from_attributes = True
      
class ChagePasswordSchema(BaseModel):
    id: Optional[str]
    current_password: str
    new_password: str
    renew_password: str
    
    @field_validator('current_password')
    def current_password_not_empty(cls, current_password):
        if not current_password:
            raise ValueError('Contraseña Actual es Requerido')
        return current_password
    
    @field_validator('current_password')
    def new_password_not_empty(cls, new_password):
        if not new_password:
            raise ValueError('Contraseña Nueva es Requerido')
        return new_password
    
    @field_validator('renew_password')
    def renew_password_password_not_empty(cls, renew_password):
        if not renew_password:
            raise ValueError('Contraseña Nueva repetida es Requerida')
        return renew_password 
   
class Users(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    
class UserResult(ObjectResult):
    data: Users

class ListUserResult(ObjectResult):
    data: List[Users]
