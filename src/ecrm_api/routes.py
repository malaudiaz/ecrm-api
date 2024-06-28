from fastapi import APIRouter

from ecrm_api.modules.login.routes import login_router

from ecrm_api.modules.users.routes.users import users_router
from ecrm_api.modules.accountingentry.routes.accrelopecategories import accountingentry_router
from ecrm_api.modules.publishmgr.routes.department import publishdepartment_router
from ecrm_api.modules.publishmgr.routes.campaign import publishcampaign_router
from ecrm_api.modules.publishmgr.routes.specialist import publishspecialist_router

api_router = APIRouter()
api_router.include_router(login_router)
api_router.include_router(users_router)
api_router.include_router(accountingentry_router)

api_router.include_router(publishcampaign_router)
api_router.include_router(publishdepartment_router)
api_router.include_router(publishspecialist_router)