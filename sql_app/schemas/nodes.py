from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import date,datetime
from enum import Enum

class action(Enum):
    search="search"
    click="click"
    good="good"
    early="early"
    impossible="impossible"

class hiddennode(BaseModel):
    create_key: str

class wordhidden(BaseModel):
    fromid: int
    toid: int
    strength: float

class hiddenhidden(BaseModel):
    fromid: int
    toid: int
    strength: float

class hiddenurl(BaseModel):
    fromid: int
    toid: int
    strength: float

class userResponseCache(BaseModel):
    id: int
    sessionvalue: str
    querys: str
    selectedurl: str
    action: action