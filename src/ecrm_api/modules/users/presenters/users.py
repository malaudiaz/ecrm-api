"""coding=utf-8."""
 
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from ecrm_api.core.presenters import ObjectResult
 
class UserBase(BaseModel):
    user_name: str
    display_name: str
    last_name: Optional[str]
    email_address: Optional[str]
    
    @field_validator('user_name')
    def user_name_not_empty(cls, user_name):
        if not user_name:
            raise ValueError('Nombre de usuario requerido')
        return user_name  

class UserCreate(UserBase):
    password: str 
    
    @field_validator('password')
    def password_not_empty(cls, password):
        if not password:
            raise ValueError('Contraseña Requerida')
        return password 

class UserShema(UserCreate):
    user_id: UUID
    is_active: bool
    changed: bool
    verify_ldap: bool
    
    created: datetime = datetime.today()
    created_by: str
    created_date: datetime = datetime.today()
    updated_by: str
    updated_date: datetime = datetime.today()
    
    last_auth: datetime = datetime.today()
    last_auth_from: str
    
    class Config:
        from_attributes = True
      
class ChagePasswordSchema(BaseModel):
    user_id: Optional[str]
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
    user_id: str
    user_name: str
    display_name: str
    email_address: str
    
class UserResult(ObjectResult):
    data: Users

class ListUserResult(ObjectResult):
    data: List[Users]
