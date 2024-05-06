from pydantic import BaseModel
from typing import Optional, Union
from datetime import date

class Post(BaseModel):
    post_id: str
    content: str
    age: int
    post_date: date
    tag_id: list
    anonymous: bool
    good: int
    early: int

class PostOut(Post):
    pass

class PostIn(Post):
    user_id: str
    impossible: int