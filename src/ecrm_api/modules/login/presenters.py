"""coding=utf-8."""
 
from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str

class AuthToken(BaseModel):
    access_token: str
    token_type: str
    
class WhoIs(BaseModel):
    user_id: str
    user_name: str
    display_name: str
