from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import date,datetime
from enum import Enum

class Feedback(Enum):
    good="good"
    early="early"
    impossible="impossible"

class Post(BaseModel):
    post_id: int
    title:str
    content: str
    age: int
    post_date: datetime
    tag_id: list
    anonymous: bool


class PostOut(Post):
    good: int
    early: int
    username: Union[str,None]=None
    user_displayedname:Union[str,None]=None

class PostHidden(Post):
    username: str
    impossible: int=0

class PostIn(BaseModel):
    title:str=Field(...,min_length=5,max_length=50)
    content: str
    age: int
    tag_id: list
    anonymous: bool

class PostInDB(Post):
    good: int=0
    early: int=0
    username: str
    impossible: int=0

class DisplayPost(BaseModel):
    post_id: int
    user_id: Optional[int]=None
    username: Optional[str]=None
    displayed_username: Optional[str]=None
    title: str
    content: str
    post_date: datetime
    tag_id: list
    anonymous: bool
    good: int
    early: int
    age: int
    certified: bool
    url: str