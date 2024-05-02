from pydantic import BaseModel
from typing import Optional, Union

class Post(BaseModel):
    post_id: str
    content: str
    age: int
    tag_id: list
    anonymous: bool
    good: int
    early: int

class PostOut(BaseModel):
    pass

class PostIn(BaseModel):
    user_id: str
    impossible: int