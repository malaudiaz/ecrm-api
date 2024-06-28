"""coding=utf-8."""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer, Unicode, DateTime, Float, Numeric
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class PublishContract(Base):
    """Class PublishContract. Manage all functionalities for PublishContract."""
 
    __tablename__ = "publish_contracts"
    __table_args__ = {'schema' : 'publishmgr'}
     
    eid = Column(String, primary_key=True, default=generate_uuid)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    created_by = Column(Unicode(24), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_by = Column(Unicode(24), nullable=False)
    
    service_name = Column(Unicode(12), nullable=False)
    publish_departament_eid = Column(String, ForeignKey("publishmgr.publish_departament.eid"), nullable=False)
    user_name = Column(Unicode(24), ForeignKey("usermgr.users.user_name"), index=True, nullable=False)
    store_code = Column(Unicode(5))
    
    partner_address_eid = Column(Unicode(24))
    partner_address_type = Column(Unicode(30))
    contact_eid = Column(Unicode(24))
    
    campaign_eid = Column(String, ForeignKey("publishmgr.publish_campaign.eid"), nullable=False)
    
    observation = Column(Unicode(250))
    
    initial_import = Column(Numeric(18,2))
    publish_import = Column(Numeric(18,2))
    discount_import = Column(Numeric(18,2))
    total_import = Column(Numeric(18,2))
    
    initial_billing_eid = Column(Unicode(24))
    initial_billing_number = Column(Unicode(24))
    initial_payment_date = Column(DateTime)
    initial_payment_system = Column(Unicode(30))
    
    publish_billing_eid = Column(Unicode(24))
    publish_billing_number = Column(Unicode(24))
    publish_billing_date = Column(DateTime)
    publish_payment_date = Column(DateTime)
    publish_payment_system = Column(Unicode(30))
    
    status = Column(Unicode(25)) #, ForeignKey("crm.comercial_states.name"))
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    