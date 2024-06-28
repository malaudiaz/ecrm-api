
"""coding=utf-8."""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode, DateTime
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class ComercialSpecialists(Base):
    """Class ComercialSpecialists. Manage all functionalities for ComercialSpecialists."""
 
    __tablename__ = "comercial_specialists"
    __table_args__ = {'schema' : 'crm'}
     
    eid = Column(String, primary_key=True, default=generate_uuid)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    created_by = Column(Unicode(24), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_by = Column(Unicode(24), nullable=False)
    
    user_name = Column(Unicode(24), ForeignKey("usermgr.users.user_name"), index=True, nullable=False)
    
    comercial_groups_eid = Column(Unicode(24), ForeignKey("crm.comercial_groups.eid"), nullable=False)
    
    status = Column(Unicode(25), ForeignKey("crm.comercial_states.name"))
    
    def dict(self):
        return {
            "eid": self.eid,
            "user_name": self.user_name,
            "comercial_groups_eid": self.comercial_groups_eid
        }
        
    