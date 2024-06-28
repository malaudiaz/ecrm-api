
"""coding=utf-8."""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode, DateTime
from ecrm_api.core.persistence.db import Base

class ComercialGroupsType(Base):
    """Class ComercialGroupsType. Manage all functionalities for ComercialGroupsType."""
 
    __tablename__ = "comercial_group_types"
    __table_args__ = {'schema' : 'crm'}
     
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    created_by = Column(Unicode(24), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_by = Column(Unicode(24), nullable=False)
    name = Column(Unicode(100), unique=True, nullable=False)
    description = Column(Unicode(150))
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
  
 

