from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi import (
    Depends,
    FastAPI,
)

from typing import Annotated
from models.users import User
from dependencies import get_current_user

from routers import posts, users

app=FastAPI(
    title="失敗なし",
    description="""
    先輩たちからの経験談。
    """,
    version="0.0.1"
)

origins=[
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/",tags=["home"])
async def root(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user:
        return {"message":"timeline of posts","detail":current_user}
    else:
        print("redirect")
        return RedirectResponse("/users/login")