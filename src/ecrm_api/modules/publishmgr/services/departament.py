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

from ecrm_api.modules.publishmgr.models.departament import PublishDepartament
from ecrm_api.modules.publishmgr.presenters.departament import PublishDepartamentBase



def new(request, publishdepartament: PublishDepartamentBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    # verificar el codigo del grupo comercial y las oficinas
    
    department_by_code = get_one_by_code(publishdepartament.code, db=db)
    if department_by_code:
        raise HTTPException(status_code=404, detail=("publishmgr.code_department_exist"))
    
    eid = str(uuid.uuid4())
    db_one_department = PublishDepartament(eid=eid, code=publishdepartament.code, name=publishdepartament.name,
                                           comercial_group_eid=publishdepartament.comercial_group_eid,
                                           store_code_legal=publishdepartament.store_code_legal, 
                                           store_code_natural=publishdepartament.store_code_natural,
                                           is_active=True)
    
    try:
        db.add(db_one_department)
        db.commit()
        result.data = eid
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        
        raise HTTPException(status_code=403, detail='Error')

def update(request, eid:str, publishdepartament: PublishDepartamentBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    # verificar el codigo del grupo comercial y las oficinas
    
    db_one_department = get_one_by_eid(eid, db=db)
    if not db_one_department:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))
    
    if publishdepartament.code and db_one_department != publishdepartament.code:
        department_by_code =  get_one_by_code(publishdepartament.code, db=db)
        if department_by_code:
            raise HTTPException(status_code=404, detail=("publishmgr.code_department_exist"))
        db_one_department.code = publishdepartament.code
    
    if publishdepartament.name and db_one_department.name != publishdepartament.name:
        db_one_department.name = publishdepartament.name
    
    if publishdepartament.comercial_group_eid and db_one_department.comercial_group_eid != publishdepartament.comercial_group_eid:
        # verificar que existe el crm
        db_one_department.comercial_group_eid = publishdepartament.comercial_group_eid
    
    if publishdepartament.store_code_legal and db_one_department.store_code_legal != publishdepartament.store_code_legal:    
        db_one_department.store_code_legal = publishdepartament.store_code_legal
        
    if publishdepartament.store_code_natural and db_one_department.store_code_natural != publishdepartament.store_code_natural:
        db_one_department.store_code_natural = publishdepartament.store_code_natural
    
    try:
        db.add(db_one_department)
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
       
def get_all(request:Request, query: str, page: int, per_page: int, db: Session):  
    # locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_from = "FROM publishmgr.publish_departament dpto "  

    str_count = "Select count(*) " + str_from
   
    str_query = "Select dpto.eid, dpto.code, dpto.name, dpto.comercial_group_eid, dpto.store_code_legal, dpto.store_code_natural " + str_from

    str_where = " WHERE dpto.is_active is True "  
    
    str_where += " AND (dpto.name ilike '%" + query + "%' OR dpto.code ilike '%" + query + "%')" if query else ''
        
    str_count += str_where
    str_query += str_where
    
    result = ObjectResult 
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=("commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    result = ObjectResult 
     
    str_query += " ORDER BY dpto.code " 
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)  
           
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
             
    lst_data = db.execute(text(str_query))
    
    result.data = [create_dict_row(item) for item in lst_data]

    # print(result.__dict__)

    return result

def create_dict_row(item):
    
    new_row = {'eid': item.eid, 'code' : item.code, 'name': item.name, 
               'comercial_group_eid': item.comercial_group_eid if item.comercial_group_eid else '', 
               'store_code_legal': item.store_code_legal if item.store_code_legal else '',  
               'store_code_natural': item.store_code_natural if item.store_code_natural else ''}
    return new_row

def get_one(request:Request, eid: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    db_one = get_one_by_eid(eid, db=db)  
    if not db_one:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))  
    
    result.data = {'eid': db_one.eid, 'code' : db_one.code, 'name': db_one.name, 
               'comercial_group_eid': db_one.comercial_group_eid if db_one.comercial_group_eid else '', 
               'store_code_legal': db_one.store_code_legal if db_one.store_code_legal else '',  
               'store_code_natural': db_one.store_code_natural if db_one.store_code_natural else ''}

    return result

def get_one_by_eid(eid: str, db: Session):  
    return db.query(PublishDepartament).filter(PublishDepartament.eid == eid).first()
        
def get_one_by_code(code: str, db: Session):  
    return db.query(PublishDepartament).filter_by(code=code, is_active=True).first()
