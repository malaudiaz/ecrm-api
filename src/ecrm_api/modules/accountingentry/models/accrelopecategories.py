"""coding=utf-8."""

import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, Integer
from ecrm_api.core.persistence.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class AccountingRelOperationsCategories(Base):
    """AccountingRelOperationsCategories """
 
    __tablename__ = "accounting_rel_operations_categories"
    __table_args__ = {'schema' : 'accountingentrymgr'}
    
    operation_type = Column(String, primary_key=True)
    operation_category_name = Column(String, primary_key=True)
    
    is_active = Column(Boolean, nullable=False, default=True)
    
    def dict(self):
        return {
            "operation_type": self.operation_type,
            "operation_category_name": self.operation_category_name,
            "is_active": self.is_active
        }
        
 