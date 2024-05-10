from typing import Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date

class Gender(str,Enum):
    f="f"
    m="m"

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str=Field(...,min_length=4,max_length=20)
    displayed_name: str

class UserInpi(BaseModel):
    birth: date
    gender: Gender
    occupation: str
    mbti: str= Field(..., max_length=4,pattern="^[IE][NS][FT][PJ]$")

class UserIntag(BaseModel):
    interested_tag: list

class UserInpw(BaseModel):
    password:str=Field(...,min_length=8)

class UserIn(User,UserInpi,UserInpw):
    pass

class UserResetPW(BaseModel):
    new_password: str

class UserCert(User):
    certified: Optional[bool]=False

class UserInDBpw(User):
    hashed_password: str

class UserInDBchar(User):
    birth: date
    gender: Gender
    occupation: str
    mbti: str= Field(..., max_length=4,pattern="^[IE][NS][FT][PJ]$")

class UserInDBtag(User):
    interested_tag: list

class UserInDB1(UserInDBchar,UserInDBpw):
    user_id: int

class UserInDB(UserInDBchar,UserInDBpw,UserCert):
    user_id: int

class UserOut(UserCert):
    pass

class Admin(BaseModel):
    username: str