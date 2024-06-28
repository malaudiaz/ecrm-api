"""coding=utf-8."""

import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class PublishSpecialists(Base):
    """PublishSpecialists """
 
    __tablename__ = "publish_specialists"
    __table_args__ = {'schema' : 'publishmgr'}
    
    eid = Column(String, primary_key=True, default=generate_uuid)
    user_name = Column(String(24), nullable=False, unique=True)
    code = Column(Unicode(10))
    
    publish_departament_eid = Column(String, ForeignKey("publishmgr.publish_departament.eid"), nullable=False)
    
    is_active = Column(Boolean, nullable=False, default=True)
    
    def dict(self):
        return {
            "eid": self.eid,
            "code": self.code,
            "user_name": self.user_name,
            "publish_departament_eid": self.publish_departament_eid,
            "is_active": self.is_active
        }
