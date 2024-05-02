from datetime import datetime, time, timedelta, date
from enum import Enum
from typing import Literal, Union, Optional, Annotated
from uuid import UUID

from fastapi.responses import RedirectResponse
from routers import users

from fastapi import (
    Body,
    Depends,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

from routers import posts, users


app=FastAPI(
    title="失敗なし",
    description="""
    先輩たちからの経験談。
    """,
    version="0.0.1"
)

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/",tags=["home"])
async def root(request:Request):
    sessionkey=request.cookies.get('sessionKey')
    if sessionkey:
        return {"displayed_name":User['displayed_name'],
                "posts":range(10)}
    else:
        RedirectResponse("/token")

@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
