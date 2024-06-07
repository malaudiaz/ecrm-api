import secrets

from pydantic import AnyHttpUrl, EmailStr, field_validator

# from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

# CORS Origins
origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:3000",
    "https://localhost",
    "https://localhost:5000",
    "https://localhost:3000",
]
