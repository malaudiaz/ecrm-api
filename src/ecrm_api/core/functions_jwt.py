from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta
from ecrm_api.core.config import settings
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from ecrm_api.modules.login.presenters import oauth2_scheme
from jose import jwt, JWTError
from ecrm_api.core.config import settings
from ecrm_api.modules.login.services import get_login_user

def expire_date(minutes: int):
    expire = datetime.now() + timedelta(minutes=minutes)
    return expire

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(minutes=1440)}, key=settings.secret, algorithm=settings.algorithm)
    return token
  
def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=settings.secret, algorithms=[settings.algorithm])
        decode(token, key=settings.secret, algorithms=[settings.algorithm])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=401)
    
def get_current_user(request):
    token = request.headers["authorization"].split(" ")[1]
    return decode(token, key=settings.secret, algorithms=[settings.algorithm])

def get_user_current(token: str = Depends(oauth2_scheme)): 
    try:
        token_decode = jwt.decode(token, key=settings.secret, algorithms=["HS256"])
        username = token_decode.get("sub")
              
        if username == None:
            raise HTTPException(status_code=401, detail="No existe el usuario", headers={"WWW-Authenticate": "Bearer"})            
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token incorreto o ha expirado", headers={"WWW-Authenticate": "Bearer"})

    user = get_login_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas", headers={"WWW-Authenticate": "Bearer"})

    return user
