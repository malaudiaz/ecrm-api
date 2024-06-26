from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ecrm_api.modules.login.services import auth
from ecrm_api.modules.login.presenters import AuthToken, User, WhoIs
from ecrm_api.core.persistence.db import get_db
from ecrm_api.core.functions_jwt import get_user_current

login_router = APIRouter(
    tags=["Autentificación"]
)

@login_router.post(
    "/login", response_model=AuthToken, summary="Autentificación en la API"
)
async def login(formdata: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth(formdata=formdata, db=db)

@login_router.get("/whois", response_model=WhoIs, summary="Información del usuario logueado")
async def get_me(user: User = Depends(get_user_current), db: Session = Depends(get_db)):
    return user

