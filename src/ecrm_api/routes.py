from fastapi import APIRouter
from ecrm_api.modules.login.routes import login_router
from ecrm_api.modules.users.routes import users_router

api_router = APIRouter()
api_router.include_router(login_router)
api_router.include_router(users_router)
