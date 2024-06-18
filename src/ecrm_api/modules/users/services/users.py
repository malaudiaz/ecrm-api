
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext

from sqlalchemy.sql import text

from jwt import encode
from ecrm_api.core.auth_bearer import decodeJWT
from ecrm_api.core.functions_jwt import get_current_user

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.responses import JSONResponse

from ecrm_api.core.config import settings
# from ecrm_api.app import _

from ecrm_api.core.persistence.db import get_ext_db, get_db

# from ecrm_api.core.persistence.db import get_db
from ecrm_api.core.presenters import BaseResult, ObjectResult
from ecrm_api.core.utils import get_result_count

from ecrm_api.modules.users.models.users import Users
from ecrm_api.modules.users.presenters.users import UserCreate, ChangePasswordSchema, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_check(passwd, min_len, max_len, level):
    RespObj = {"success": True, "message": "Contraseña correcta"}

    if level > 0:
      
        RejectSym =['$', '@', '#', '%', '^']
        AcceptSym = ['!', '*', '.', '+', '-', '_', '?', ';', ':', '&', '=']

        if level == 1:
            if len(passwd) < min_len:
                RespObj["success"] = False
                RespObj["message"] = "La contraseña no debe tener menos de " + str(min_len) + " carácteres"
                
            if len(passwd) > max_len:
                RespObj["success"] = False
                RespObj["message"] = "La contraseña no debe exceder los " + str(max_len) + " carácteres"

        if level == 2:
            if len(passwd) < min_len:
                RespObj["success"] = False
                RespObj["message"] = "La contraseña no debe tener menos de " + str(min_len) + " carácteres"
                
            if len(passwd) > max_len:
                RespObj["success"] = False
                RespObj["message"] = "La contraseña no debe exceder los " + str(max_len) + " carácteres"

            if not any(char.isdigit() for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contar con al menos un Número"
                
            if not any(char.isupper() for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contar con al menos una Mayúscula"
                
            if not any(char.islower() for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contar con al menos una Minúscula"


        if level == 3:
            if len(passwd) < min_len:
                RespObj["success"] = False
                RespObj["message"] = "La contraseña no debe tener menos de " + str(min_len) + " carácteres"
                
            if len(passwd) > max_len:
                RespObj["success"] = False
                RespObj["message"] = "La contraseña no debe exceder los " + str(max_len) + " carácteres"

            if not any(char.isdigit() for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contar con al menos un Número"
                
            if not any(char.isupper() for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contar con al menos una Mayúscula"
                
            if not any(char.islower() for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contar con al menos una Minúscula"


            if not any(char in AcceptSym for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña debe contener al menos un carácter especial"
                
            if any(char in RejectSym for char in passwd):
                RespObj["success"] = False
                RespObj["message"] = "La contraseña contiene carácteres no permitidos"

    return RespObj

def get_one(user_id: str, db: Session):  
    return db.query(Users).filter(Users.user_id == user_id).first()

def get_one_by_user_name(user_name: str, db: Session):  
    return db.query(Users).filter(Users.user_name == user_name, Users.is_active == True).first()

def get_one_by_id(request: Request, user_id: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    result = BaseResult 
    
    db_user = get_one(user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail=("auth.not_found"))
    
    result.data = db_user.dict()
    return result

def get_all(request:Request, page: int, per_page: int, criteria_value: str, db: Session): #, ext_db: Session):    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_where = "WHERE is_active=True " 
    str_from = "FROM usermgr.users "
            
    str_count = "Select count(*) " + str_from
    str_query = "Select user_id, user_name, display_name, email_address, last_auth, last_auth_from, verify_ldap " + str_from

    ext_db = next(get_ext_db())
    
    str_search = ''
    if criteria_value:
        str_search = "AND (user_name ilike '%" + criteria_value + "%' OR display_name ilike '%" + criteria_value +\
            "%' OR email_address ilike '%" + criteria_value + "%')"
        str_where += str_search
 
    # search_query = '{0}'.format(query)
    # search_chain = (User.email.ilike(search_query), User.username.ilike(search_query))

    # return or_(*search_chain)

    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=("commun.invalid_param"))
    
    str_count += str_where 
    str_query += str_where
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY user_name "
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(text(str_query)).all()
    # result.data = [create_dict_row(item) for item in lst_data]
    lsr_result_data = [create_dict_row(item) for item in lst_data]
    
    str_domino = "SELECT * FROM federations.federations ORDER BY id ASC"
    lst_dom = ext_db.execute(text(str_domino)).all()
    
    lst_all_dom = []
    for item in lst_dom:
        lst_all_dom.append({'id': item.id, 'name': item.name})
    
    result.data = {'users': lsr_result_data, 'fed': lst_all_dom}
    
    return result

def create_dict_row(item):
    
    new_row = {'user_id': item.user_id, 'user_name' : item.user_name, 'display_name': item.display_name, 
               'email_address': item.email_address if item.email_address else '', 
               'last_auth': item.last_auth if item.last_auth else '',  
               'last_auth_from': item.last_auth_from if item.last_auth_from else '',
               'verify_ldap': item.verify_ldap if item.verify_ldap else False}
    return new_row
 
def new(request: Request, db: Session, user: UserCreate):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult 
    
    #verificar que el nombre de usuario no existe en Base de Datos, ver despues si tengo en cuante activo o no.
    str_user = "SELECT count(user_name) FROM usermgr.users where user_name = '" + user.user_name + "' "
    amount_user = db.execute(text(str_user)).fetchone()[0]
    if amount_user > 0:
        raise HTTPException(status_code=404, detail=("users.already_exist"))  
    
    pass_check = password_check(user.password, settings.pwd_length_min, settings.pwd_length_max, settings.pwd_level)   
    if not pass_check['success']:
        raise HTTPException(status_code=404, detail=("users.data_error") + pass_check['message'])             

    user.password = pwd_context.hash(user.password)  
    db_user = Users(user_name=user.user_name,  display_name=user.display_name, email_address=user.email_address, 
                    password=user.password, created=datetime.now(), created_date=datetime.now(), updated_date=datetime.now(),
                    created_by='mgt', updated_by='mgt', last_auth=None, last_auth_from=None,
                    is_active=True, changed=False, verify_ldap=True)
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        result.data = {'user_id': db_user.user_id}
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        raise HTTPException(status_code=403, detail="users.new_user_error") 
    
def delete(request: Request, user_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult
    currentUser = get_current_user(request)
    
    db_user = get_one(user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail=("auth.not_found"))
    
    try:
        db_user.is_active = False
        db_user.updated_by = currentUser['user_name']
        db_user.updated_date = datetime.now()
        db.commit()
        result.data = {'user_id': user_id}
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=("users.imposible_delete"))
    
def update(request: Request, user_id: str, user: UserUpdate, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult
    currentUser = get_current_user(request)
       
    db_user = get_one(user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail=("auth.not_found"))
    
    if user.display_name != db_user.display_name:
        db_user.display_name = user.display_name
        
    if user.email_address != db_user.email_address:
        db_user.email_address = user.email_address
        
    if user.verify_ldap != db_user.verify_ldap:
        db_user.verify_ldap = user.verify_ldap
    
    db_user.updated_by = currentUser['user_name']
    db_user.updated_date = datetime.now()
            
    try:
        db.add(db_user)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "users.already_exist"))
        
def change_password(request: Request, db: Session, password: ChangePasswordSchema):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = BaseResult
    
    # if el id viene vacio cojo el usario logueado
    if not password.user_id:
        currentUser = get_current_user(request)
        one_user = get_one_by_user_name(username=currentUser['user_name'], db=db)
    else:
        one_user = get_one(user_id=password.user_id, db=db)
        
    if not one_user:
        raise HTTPException(status_code=404, detail=("users.not_found"))
    
    if not password.by_data_migration: 
        if not pwd_context.verify(password.current_password, one_user.password):
            raise HTTPException(status_code=405, detail=("users.wrong_password"))
        
    # verificar que las contrasenas nuevas son iguales
    if str(password.new_password) != str(password.renew_password):
        raise HTTPException(status_code=404, detail=("users.check_password"))
    
    #verificando que tenga la estructura correcta
    pass_check = password_check(password.new_password, 8, 15, 1)   
    if not pass_check['success']:
        raise HTTPException(status_code=404, detail=("users.new_password_incorrect") + pass_check['message']) 
    
    #cambiando el paswword al usuario
    one_user.password = pwd_context.hash(password.new_password)
    
    # one_user.updated_by = currentUser['user_name']
    one_user.updated_date = datetime.now()
    
    try:
        db.add(one_user)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        raise HTTPException(status_code=400, detail=("users.change_password_error"))
        
   