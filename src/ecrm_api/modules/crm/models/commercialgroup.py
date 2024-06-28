
"""coding=utf-8."""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode, DateTime
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class ComercialGroups(Base):
    """Class ComercialGroups. Manage all functionalities for ComercialGroups."""
 
    __tablename__ = "comercial_groups"
    __table_args__ = {'schema' : 'crm'}
     
    eid = Column(String, primary_key=True, default=generate_uuid)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    created_by = Column(Unicode(24), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_by = Column(Unicode(24), nullable=False)
    name = Column(Unicode(120), nullable=False)
    description = Column(Unicode(120))
    
    comercial_gruops_type_id = Column(Integer, ForeignKey("crm.comercial_group_types.id"), nullable=False)
    
    code = Column(Unicode(6))
    str_code = Column(Unicode(4))
    
    business_units_eid = Column(Unicode(24), nullable=True)
    
    parent_eid = Column(Unicode(24), ForeignKey("crm.comercial_groups.eid"), index=True, nullable=False)
    
    status = Column(Unicode(25), ForeignKey("crm.comercial_states.name"))
    
    state_id = Column(Integer, nullable=True)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    