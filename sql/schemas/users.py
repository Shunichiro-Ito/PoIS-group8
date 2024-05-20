from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date

class Gender(str,Enum):
    f="f"
    m="m"

class interest_tag(BaseModel):
    tag_id: int
    user_id: int
    tag_name: str

class url(BaseModel):
    url: str
    id: int
    type: str="user"

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

class UserCert(BaseModel):
    user_id: Union[int,None]
    username: Union[str,None]
    certified: Optional[bool]=False

class UserInDBpw(BaseModel):
    user_id: Union[int,None]
    username: Union[str,None]
    hashed_password: str

class UserInDBchar(BaseModel):
    user_id: Union[int,None]
    username: Union[str,None]
    birth: date
    gender: Gender
    occupation: str
    mbti: str= Field(..., max_length=4,pattern="^[IE][NS][FT][PJ]$")

class UserInDBtag(BaseModel):
    user_id: Union[int,None]
    username: Union[str,None]
    interested_tag: list

    class Config:
        #orm_mode=True
        pass

class UserInDB1(UserInDBchar,UserInDBpw):
    user_id: int

    class Config:
        #orm_mode=True
        pass

class UserInDB(UserInDBchar,UserInDBpw,UserCert):
    user_id: int
    displayed_name: str

class UserOut(UserCert):
    displayed_name: str

class Admin(BaseModel):
    username: str

class UserResponseCache(BaseModel):
    sessionvalue: Any
    querys: Any
    selectedurl: Optional[str]=None
    action: str