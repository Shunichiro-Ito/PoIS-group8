from typing import Optional
from pydantic import BaseModel

class user_login(BaseModel):
    username: str
    password: str