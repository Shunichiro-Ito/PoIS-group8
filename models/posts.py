from pydantic import BaseModel
from typing import Optional, Union
from datetime import date,datetime

class Post(BaseModel):
    post_id: int
    content: str
    age: int
    post_date: datetime
    tag_id: list
    anonymous: bool


class PostOut(Post):
    good: int
    early: int

class PostOut2(PostOut):
    username: str
    user_displayedname:str

class PostHidden(Post):
    username: str
    impossible: int=0

class PostIn(BaseModel):
    content: str
    age: int
    tag_id: list
    anonymous: bool

class PostInDB(Post):
    good: int=0
    early: int=0
    username: str
    impossible: int=0