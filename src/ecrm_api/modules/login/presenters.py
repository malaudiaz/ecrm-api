"""coding=utf-8."""
 
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Union

oauth2_scheme = OAuth2PasswordBearer("/api/v1/login")

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None    
    email: Union[str, None] = None   
    disabled: Union[bool, None] = None 
    
class UserInDB(User):
    hashed_password: str  

class UserLogin(BaseModel):
    username: str
    password: str

class AuthToken(BaseModel):
    access_token: str
    token_type: str
    
class WhoIs(BaseModel):
    sub: str
    exp: int