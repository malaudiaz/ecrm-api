
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext


from sqlalchemy.sql import text

from ecrm_api.modules.users.models import Users 

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
    print(user)
    return user

def auth(request: Request, db: Session, user: UserLogin):
    # locale = request.headers["accept-language"].split(",")[0].split("-")[0]

    str_query = "SELECT us.id user_id, us.username, us.first_name, us.last_name, pro.photo, " +\
        "us.is_active, password, pro.profile_type " +\
        "FROM enterprise.users us inner join enterprise.profile_member pro ON pro.id = us.id " +\
        "WHERE us.username = '" + user.username + "' "
             
   
    lst_data = db.execute(text(str_query))
       
    if not lst_data:
        raise HTTPException(
            status_code=404, detail="auth.not_found")

    user_id, username, first_name = '', '', ''
    password = ''
    is_active = False
    for item in lst_data:
        user_id, username = item.user_id, item.username
        first_name = item.first_name
        is_active = item.is_active
        password = item.password

    if is_active is False:
        raise HTTPException(status_code=404, detail="auth.not_registered")

    if pwd_context.verify(user.password, password):
        token_data = {"username": username, "user_id": user_id, "name": first_name}

        response = JSONResponse(content={"access_token":write_token(data=token_data), "token_type":"bearer"},
                                status_code=200)

        return response
    else:
        raise HTTPException(status_code=404, detail="auth.wrong_password")
