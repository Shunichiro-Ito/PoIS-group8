from typing import Union
from fastapi import (
    FastAPI,
    Cookie
    )

app=FastAPI(
    title="失敗なし",
    description="""
    先輩たちからの経験談。
    """,
    version="0.0.1"
)

@app.get("/",tags=["home"])
async def root():
    return {"message":"hello"}

# Route to user
@app.get("/users/{user_id}")
async def userProfile(user_id:int):
    
    return {"message":"hello"}

@app.post("/login")
async def login(user_login):
    return {"message":"hello"}



# Route to post
