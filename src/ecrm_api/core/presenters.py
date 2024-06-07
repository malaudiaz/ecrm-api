"""coding=utf-8."""

from typing import List, Any
from pydantic import BaseModel

class BaseResult(BaseModel):
    success: bool = True
    detail: str = 'Operación satisfactoria'

class ObjectResult(BaseResult):
    data: Any
