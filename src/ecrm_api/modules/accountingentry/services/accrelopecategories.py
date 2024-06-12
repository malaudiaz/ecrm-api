
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext

from sqlalchemy.sql import text

from jwt import encode
from ecrm_api.core.auth_bearer import decodeJWT

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.responses import JSONResponse

from ecrm_api.core.config import settings
# from ecrm_api.app import _

from ecrm_api.core.persistence.db import get_db
from ecrm_api.core.presenters import BaseResult, ObjectResult

from ecrm_api.modules.accountingentry.models.accrelopecategories import AccountingRelOperationsCategories
from ecrm_api.modules.accountingentry.presenters.accrelopecategories import AccountingRelOperationsCategoriesBase


def new(request, opecategory: AccountingRelOperationsCategoriesBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    #verificar que no se encuentre ya esa categoria en esa tipo de operación
    res = ObjectResult
    
    db_one = get_one_by_operation_category(opecategory.operation_type, opecategory.operation_category_name, db=db)  
    if db_one:
        raise HTTPException(status_code=404)
        # raise HTTPException(status_code=404, detail=_(locale, "accountingentry.ope_type_category_exist"))
    
    db_one_ope = AccountingRelOperationsCategories(operation_type=opecategory.operation_type, 
                                                   operation_category_name=opecategory.operation_category_name, is_active=True)
    
    try:
        db.add(db_one_ope)
        db.commit()
        res.data = db_one_ope.operation_type
        return res
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        
        raise HTTPException(status_code=403, detail='Error')
    
def delete(request, operation_type:str, operation_category_name: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ObjectResult 
    
    db_one = get_one_by_operation_category(operation_type, operation_category_name, db=db)  
    if not db_one:
        raise HTTPException(status_code=404)
        # raise HTTPException(status_code=404, detail=_(locale, "accountingentry.ope_type_category_exist"))
    
    if not db_one:
        raise HTTPException(status_code=404)
    
    try:
        db_one.is_active = False
        db.commit()
        return result
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404)
        # raise HTTPException(status_code=404, detail=_(locale, "club.imposible_delete"))
            
        
def get_all(request:Request, page: int, per_page: int, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_from = "FROM events.tourney tou " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id " +\
        "JOIN federations.federations fed ON fed.id = tou.federation_id " +\
        "LEFT JOIN resources.city city ON city.id = tou.city_id " +\
        "LEFT JOIN resources.country country ON country.id = city.country_id " 
    
    str_count = "Select count(*) " + str_from
    str_query = "Select tou.id, tou.modality, tou.name, tou.summary, tou.start_date, " +\
        "city.id  as city_id, city.name as city_name, inscription_import, amount_rounds, main_location, " +\
        "tou.status_id, sta.name as status_name, sta.description as status_description, tou.image " + str_from
    
    str_where = " WHERE sta.name != 'CANCELLED' "  
    
    str_where += " AND (tou.name ilike '%" + criteria_value + "%' OR tou.modality ilike '%" +  criteria_value + "%'" +\
        " OR tou.summary ilike '%" + criteria_value + "%'  OR city.name ilike '%" + criteria_value + \
        "%' OR main_location ilike '%" + criteria_value + "%') " if criteria_value else ''
    
    str_count += str_where
    str_query += str_where
    
    result = ObjectResult
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    # result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    # str_query += " ORDER BY start_date " 
    
    # if page != 0:
    #     str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    # lst_data = db.execute(str_query)
    
    # result.data = [create_dict_row(item, api_uri=api_uri) for item in lst_data]
    
    return result
  

def get_one_by_operation_category(operation_type: str, operation_category_name: str, db: Session):  
    return db.query(AccountingRelOperationsCategories).filter(AccountingRelOperationsCategories.operation_type == operation_type)\
        .filter(AccountingRelOperationsCategories.operation_category_name == operation_category_name)\
        .filter(AccountingRelOperationsCategories.is_active is True).first()
