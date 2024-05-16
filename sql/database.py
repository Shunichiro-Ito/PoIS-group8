from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sys
from sqlalchemy.orm import (sessionmaker, relationship, scoped_session)


sys.dont_write_bytecode = True

#setting db connection
url = "mysql+pymysql://root:group_8@localhost:3306/failure_story_db?charset=utf8"
engine = create_engine(url, echo=False, pool_recycle=10)

#create session
def create_new_session():
    return  scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine))

SessionLocal = create_new_session()

Base = declarative_base()