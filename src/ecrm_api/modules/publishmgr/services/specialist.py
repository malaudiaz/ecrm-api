import uuid

from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext

from sqlalchemy.sql import text, exists, or_

from jwt import encode
from ecrm_api.core.auth_bearer import decodeJWT

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.responses import JSONResponse

from ecrm_api.core.config import settings
from ecrm_api.core.utils import get_result_count

from ecrm_api.core.presenters import BaseResult, ObjectResult

from ecrm_api.modules.publishmgr.models.specialist import PublishSpecialists
from ecrm_api.modules.publishmgr.presenters.specialist import PublishSpecialistBase

from ecrm_api.modules.publishmgr.services.departament import get_one_by_eid as get_departament

def new(request, publishspecialist: PublishSpecialistBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    db_one_department = get_departament(publishspecialist.publish_departament_eid, db=db)
    if not db_one_department:
        raise HTTPException(status_code=404, detail=("publishmgr.department_not_exist"))
    
    specialist_by_code =  get_one_by_code(publishspecialist.code, db=db)
    if specialist_by_code:
        raise HTTPException(status_code=404, detail=("publishmgr.code_specialist_exist"))
        
    eid = str(uuid.uuid4())
    db_one_specialist = PublishSpecialists(eid=eid, code=publishspecialist.code, user_name=publishspecialist.user_name,
                                           publish_departament_eid=publishspecialist.publish_departament_eid,
                                           is_active=True)
    
    try:
        db.add(db_one_specialist)
        db.commit()
        result.data = eid
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        
        raise HTTPException(status_code=403, detail='Error')

def update(request, eid:str, publishspecialist: PublishSpecialistBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    
    db_one_specialist = get_one_by_eid(eid, db=db)
    if not db_one_specialist:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))
    
    if publishspecialist.code and db_one_specialist != publishspecialist.code:
        specialist_by_code =  get_one_by_code(publishspecialist.code, db=db)
        if specialist_by_code:
            raise HTTPException(status_code=404, detail=("publishmgr.code_specialist_exist"))
        db_one_specialist.code = publishspecialist.code
    
    if publishspecialist.user_name and db_one_specialist.user_name != publishdepartament.user_name:
        db_one_specialist.user_name = publishdepartament.user_name
    
    if publishdepartament.publish_departament_eid and db_one_specialist.publish_departament_eid != publishdepartament.publish_departament_eid:
        # verificar que existe el crm
        db_one_specialist.db_one_specialist = publishdepartament.db_one_specialist
    
    try:
        db.add(db_one_specialist)
        db.commit()
        result.data = eid
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        
        raise HTTPException(status_code=403, detail='Error')
        
def delete(request, eid:str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    db_one = get_one_by_eid(eid, db=db)  
    if not db_one:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))
    
    try:
        db_one.is_active = False
        db.commit()
        return result
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404)
       
def get_all(request:Request, page: int, per_page: int, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_from = "FROM publishmgr.publish_specialists spe " +\
        "JOIN publishmgr.publish_departament dpto ON dpto.eid = spe.publish_departament_eid "  
    
    str_count = "Select count(*) " + str_from
    str_query = "Select spe.eid, spe.code, spe.user_name, spe.publish_departament_eid, dpto.name as departament_name " + str_from
    
    str_where = " WHERE spe.is_active is True "  
    
    str_where += " AND (spe.user_name ilike '%" + criteria_value +\
        "%' OR dpto.name ilike '%" + criteria_value + "%'" + "OR spe.code ilike '%" + criteria_value + "%')" if criteria_value else ''
    
    # search_query = '{0}'.format(criteria_value)
    # search_chain = (PublishDepartament.name.ilike(search_query), PublishDepartament.code.ilike(search_query))
    # str_where = or_(*search_chain)
    
    str_count += str_where
    str_query += str_where
    
    result = ObjectResult 
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=("commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY spe.code " 
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(text(str_query))
    
    result.data = [create_dict_row(item) for item in lst_data]
    
    return result

def create_dict_row(item):
    
    new_row = {'eid': item.eid, 'code' : item.code, 'user_name': item.name, 'display_name': '',
               'publish_departament_eid': item.publish_departament_eid if item.publish_departament_eid else '', 
               'publish_departament_name': item.departament_name if item.departament_name else ''}
    return new_row

def get_one(request:Request, eid: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    db_one = get_one_by_eid(eid, db=db)  
    if not db_one:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))  
    
    result.data = {'eid': db_one.eid, 'code' : db_one.code, 'user_name': db_one.user_name, 
               'publish_departament_eid': db_one.publish_departament_eid if db_one.publish_departament_eid else '', 
               'publish_departament_name': db_one.publish_departament_eid if db_one.publish_departament_eid else ''}

    return result

def get_one_by_eid(eid: str, db: Session):  
    return db.query(PublishSpecialists).filter(PublishSpecialists.eid == eid).first()
        
def get_one_by_code(code: str, db: Session):  
    return db.query(PublishSpecialists).filter_by(code=code, is_active=True).first()
