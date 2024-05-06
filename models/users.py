from typing import Optional, Union
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import date

class Gender(str,Enum):
    f="f"
    m="m"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    displayed_name: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserInpi(BaseModel):
    birth: date
    gender: Gender
    occupation: str
    mbti: str

class UserIntag(BaseModel):
    interested_tag: list

class UserInpw(BaseModel):
    password:str

class UserIn(User,UserInpi,UserInpw):
    pass

class UserResetPW(BaseModel):
    new_password: str

class UserInDBpw(User):
    hashed_password: str

class UserInDBchar(User):
    birth: date
    gender: Gender
    occupation: str
    mbti: str

class UserInDBtag(User):
    interested_tag: list

class UserInDB(UserInDBchar,UserInDBpw,):
    pass

class UserOut(User):
    pass
