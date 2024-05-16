from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sys
from sqlalchemy.orm import (sessionmaker, relationship, scoped_session)


sys.dont_write_bytecode = True

#setting db connection
user = "user1"
password = "PoIS-group8"
host = "ip-172-31-93-14.ec2.internal:3306"
db_name = ""

#url = f"mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8"
url = f'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}?charset=utf8'
#url = "mysql+pymysql://root:group_8@localhost:3306/failure_story_db?charset=utf8"
engine = create_engine(url, echo=False, pool_recycle=10)

#create session
def create_new_session():
    return  scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine))

SessionLocal = create_new_session()

Base = declarative_base()