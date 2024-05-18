from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import date,datetime
from enum import Enum

class Feedback(Enum):
    good="good"
    early="early"
    impossible="impossible"

class gender(Enum):
    f="f"
    m="m"

class Post(BaseModel):
    post_id: int
    title:str
    content: str
    age: int
    post_date: datetime
    tag_id: int
    anonymous: bool

    class Config:
        orm_mode = True

class Post_v_tfidf(BaseModel):
    post_id: int
    tfidf_0: float
    tfidf_1: float
    tfidf_2: float
    tfidf_3: float
    tfidf_4: float
    tfidf_5: float
    tfidf_6: float
    tfidf_7: float
    tfidf_8: float
    tfidf_9: float
    tfidf_10: float
    tfidf_11: float
    tfidf_12: float
    tfidf_13: float
    tfidf_14: float
    tfidf_15: float
    tfidf_16: float
    tfidf_17: float
    tfidf_18: float
    tfidf_19: float

class Post_v_Writers_initialdata(BaseModel):
    user_id: int
    post_id: int
    category_id: int

class Post_v_Writers_dinamicdata(BaseModel):
    user_id: int
    post_id: int
    category_id: int
    age: int
    gender: gender
    occupation: str
    mbti: str

class Post_v_Readers(BaseModel):
    user_id: int
    post_id: int
    feedback: Feedback

class url(BaseModel):
    url: str
    id: int
    type: str="user"

class Category(BaseModel):
    category_id: int
    category_name: str

class PostIn(BaseModel):
    title:str=Field(...,min_length=5,max_length=50)
    content: str
    age: int
    tag_id: list
    anonymous: bool

class PostInDB(Post):
    good: int=0
    early: int=0
    user_id: int
    impossible: int=0

class PostInDBfeedback(BaseModel):
    post_id: int
    good: int
    early: int
    impossible: int