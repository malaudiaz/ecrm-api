"""coding=utf-8."""

import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class PublishDepartament(Base):
    """PublishDepartament """
 
    __tablename__ = "publish_departament"
    __table_args__ = {'schema' : 'publishmgr'}
    
    eid = Column(String, primary_key=True, default=generate_uuid)
    code = Column(Unicode(10), nullable=False)
    name = Column(Unicode(120), nullable=False)
    comercial_group_eid = Column(Unicode(24), nullable=True) #, ForeignKey("crm.comercial_groups.eid"), index=True, nullable=True)
    
    store_code_legal = Column(Unicode(6))
    store_code_natural = Column(Unicode(6))
    
    is_active = Column(Boolean, nullable=False, default=True)
    
    def dict(self):
        return {
            "eid": self.eid,
            "code": self.code,
            "name": self.name,
            "comercial_group_eid": self.comercial_group_eid,
            "store_code_legal": self.store_code_legal,
            "store_code_natural": self.store_code_natural,
            "is_active": self.is_active
        }
        
