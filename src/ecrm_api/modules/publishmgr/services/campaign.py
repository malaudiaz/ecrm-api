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

from ecrm_api.modules.publishmgr.models.campaign import PublishCampaign
from ecrm_api.modules.publishmgr.presenters.campaign import PublishCampaignBase



def new(request, publishcampaign: PublishCampaignBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    eid = str(uuid.uuid4())
    db_one_campaign = PublishCampaign(eid=eid, year=publishcampaign.year, name=publishcampaign.name, is_active=True)
    
    try:
        db.add(db_one_campaign)
        db.commit()
        result.data = eid
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        
        raise HTTPException(status_code=403, detail='Error')

def update(request, eid:str, publishcampaign: PublishCampaignBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    
    db_one_campaign = get_one_by_eid(eid, db=db)
    if not db_one_campaign:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))
    
    if publishcampaign.year and db_one_campaign != publishcampaign.year:
        db_one_campaign.year = publishcampaign.year
    
    if publishcampaign.name and db_one_campaign.name != publishcampaign.name:
        db_one_campaign.name = publishcampaign.name
    
    try:
        db.add(db_one_campaign)
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
       
    str_from = "FROM publishmgr.publish_campaign camp "  

    str_count = "Select count(*) " + str_from
   
    str_query = "Select camp.eid, camp.year, camp.name " + str_from

    str_where = " WHERE camp.is_active is True "  
    
    str_where += " AND (camp.name ilike '%" + query + "%' OR camp.year ilike '%" + query + "%')" if query else ''
        
    str_count += str_where
    str_query += str_where
    
    result = ObjectResult 
     
    str_query += " ORDER BY camp.year " 
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)  
           
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
             
    lst_data = db.execute(text(str_query))
    
    result.data = [create_dict_row(item) for item in lst_data]

    # print(result.__dict__)

    return result

def create_dict_row(item):
    
    new_row = {'eid': item.eid, 'year' : item.year, 'name': item.name}
    return new_row

def get_one(request:Request, eid: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    db_one = get_one_by_eid(eid, db=db)  
    if not db_one:
        raise HTTPException(status_code=404, detail=("publishmgr.not_exist"))  
    
    result.data = {'eid': db_one.eid, 'year' : db_one.year, 'name': db_one.name}

    return result

def get_one_by_eid(eid: str, db: Session):  
    return db.query(PublishCampaign).filter(PublishCampaign.eid == eid).first()
        
