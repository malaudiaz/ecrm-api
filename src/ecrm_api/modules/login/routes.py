from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ecrm_api.modules.login.services import auth
from ecrm_api.core.auth_bearer import JWTBearer
from ecrm_api.core.functions_jwt import get_current_user
from fastapi.responses import JSONResponse
from ecrm_api.modules.login.presenters import UserLogin, AuthToken, WhoIs
from ecrm_api.core.persistence.db import get_db

login_router = APIRouter(
    tags=["Autentificación"],
)

@login_router.post(
    "/login", response_model=AuthToken, summary="Autentificación en la API"
)
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    return auth(request=request, db=db, user=user)

@login_router.get(
    "/whois",
    response_model=WhoIs,
    summary="Obtiene información del usuario autentificado",
    dependencies=[Depends(JWTBearer())],
)
async def get_me(request: Request):
    user = get_current_user(request)
    return JSONResponse(
        {
            "user_id": user["user_id"],
            "username": user["username"],
            "name": user["name"],
        },
        status_code=200,
    )
