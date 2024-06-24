
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext


from sqlalchemy.sql import text

from ecrm_api.modules.users.models.users import Users 

from jwt import encode
from ecrm_api.core.auth_bearer import decodeJWT

from sqlalchemy.orm import Session
from ecrm_api.modules.login.presenters import UserLogin
from fastapi.responses import JSONResponse

from ecrm_api.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def expire_date(minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    return expire


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(minutes=1440)}, key=settings.secret, algorithm="HS256")
    return token


def get_login_user(request: Request):
    token = request.headers['authorization'].split(' ')[1]
    user = decodeJWT(token)
    return user

def auth(request: Request, db: Session, user: UserLogin):
    # locale = request.headers["accept-language"].split(",")[0].split("-")[0]

    str_query = "SELECT us.user_id, us.user_name, us.display_name, us.is_active, password " +\
        "FROM usermgr.users us "+\
        "WHERE us.user_name = '" + user.username + "' "
             
   
    lst_data = db.execute(text(str_query))
       
    if not lst_data:
        raise HTTPException(
            status_code=404, detail="auth.not_found")

    user_id, user_name, display_name = '', '', ''
    password = ''
    is_active = False
    for item in lst_data:
        user_id, user_name = item.user_id, item.user_name
        display_name = item.display_name
        is_active = item.is_active
        password = item.password

    if is_active is False:
        raise HTTPException(status_code=404, detail="auth.not_registered")

    if pwd_context.verify(user.password, password):
        token_data = {"user_name": user_name, "id": user_id, "name": display_name, "profile":'', 'image':''}

        response = JSONResponse(content={"access_token":write_token(data=token_data), "token_type":"bearer", "token_data": token_data},
                                status_code=200)

        return response
    else:
        raise HTTPException(status_code=404, detail="auth.wrong_password")
