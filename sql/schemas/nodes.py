from pydantic import BaseModel, Field
from typing import Any, Optional, Union
from datetime import date,datetime
from enum import Enum

class action(Enum):
    search="search"
    click="click"
    good="good"
    early="early"
    impossible="impossible"

class hiddennode(BaseModel):
    id:int
    create_key: str
    layer: int

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

class userResponseCacheIn(BaseModel):
    sessionvalue: Any
    querys: Any
    selectedurl: Union[str,None]
    action: action

class userResponseCacheOut(BaseModel):
    id: int
    sessionvalue: Any
    querys: Any
    selectedurl: Union[str,None]
    action: action