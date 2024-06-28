"""coding=utf-8."""

import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class PublishCampaign(Base):
    """PublishCampaign """
 
    __tablename__ = "publish_campaign"
    __table_args__ = {'schema' : 'publishmgr'}
    
    eid = Column(String, primary_key=True, default=generate_uuid)
    year = Column(Unicode(4))
    name = Column(Unicode(120))
    
    is_active = Column(Boolean, nullable=False, default=True)
    
    def dict(self):
        return {
            "eid": self.eid,
            "year": self.year,
            "name": self.name,
            "is_active": self.is_active
        }
        