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

class UserIn(User):
    password:str

class UserInDB(User):
    hashed_password: str
    birth: date
    gender: Gender
    occupation: str
    mbti: str
    interested_tag: list

class UserOut(User):
    pass
