

import math

from sqlalchemy.orm import Session
from sqlalchemy import text

from ecrm_api.core.presenters import BaseResult, ObjectResult

def get_result_count(page: int, per_page: int, str_count: str, db: Session): 
    if page != 0:
        result = ObjectResult
        result.page = page
        result.per_page = per_page
        result.total = db.execute(text(str_count)).scalar()
        result.total_pages=result.total/result.per_page if (result.total % result.per_page == 0) else math.trunc(result.total / result.per_page) + 1
    else:
        result = BaseResult()
               
    return result
