"""coding=utf-8."""

from typing import List, Any, Optional
from pydantic import BaseModel

class BaseResult(BaseModel):
    success: bool = True
    status_code: str = '200'
    detail: str = 'Operación satisfactoria'
    data: Any = {}
class ObjectResult(BaseResult):
    page: Optional[int] = 0
    per_page: Optional[int] = 0
    total: Optional[int] = 0
    total_pages: Optional[int] = 0
   
    