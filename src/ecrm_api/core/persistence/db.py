# db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ecrm_api.core.config import settings
 
SQLALCHEMY_DATABASE_URL = settings.database_uri
SQLALCHEMY_EXT_DATABASE_URL = settings.ext_db_uri

main_engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

ext_engine = create_engine(
    SQLALCHEMY_EXT_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, bind=main_engine)
SessionExt = sessionmaker(autocommit=False, bind=ext_engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_ext_db():
    db = SessionExt()
    try:
        yield db
    finally:
        db.close()

