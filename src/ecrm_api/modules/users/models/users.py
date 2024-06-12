"""coding=utf-8."""

import uuid
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, DateTime, Date
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Users(Base):
    """Users Class contains standard information for a User."""
 
    __tablename__ = "users"
    __table_args__ = {'schema' : 'usermgr'}
    
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(24), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    
    created = Column(DateTime, nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    created_by = Column(String(24), ForeignKey("usermgr.users.user_name"), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_by = Column(String(24), ForeignKey("usermgr.users.user_name"), nullable=False)
    
    last_auth = Column(DateTime, nullable=False)
    last_auth_from = Column(String(18), nullable=True)
    
    changed = Column(Boolean, nullable=True, default=False)
    is_active = Column(Boolean, nullable=True, default=True)
    verify_ldap = Column(Boolean, nullable=True, default=True)
    
    def dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "display_name": self.display_name,
            "email_address": self.email_address,
            "last_auth": self.last_auth,
            "last_auth_from": self.last_auth_from,
            "is_active": self.is_active,
            "verify_ldap": self.verify_ldap
        }
