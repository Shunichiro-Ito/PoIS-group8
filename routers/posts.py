from fastapi import APIRouter, Depends,HTTPException,status,Header,Response,Request,Form
from fastapi.responses import RedirectResponse
from typing import Literal, Annotated,Union
from search.searchengine import searcher
from dependencies import (
    oauth2_scheme,
    get_current_user,
    get_posts_by_user,
    get_user,
    get_a_post,
    upload_post_db,
    updateFeedback,
    updatesession,
)

from fastapi_pagination import LimitOffsetPage, paginate
from fastapi_pagination.links import Page
from fastapi_pagination.customization import (
    CustomizedPage,
    UseExcludedFields,
    UseFieldsAliases,
    UseIncludeTotal,
    UseModelConfig,
    UseName,
    UseOptionalParams,
    UseParams,
    UseParamsFields,
)

#from sqlalchemy.orm import Session
#from sql.database import SessionLocal
#from sql import crud
from fakedb import fake_posts_db,fake_post_user_db,fake_users_db,fake_feedback_db
from models.users import User,Token,Session
from models.posts import PostIn, Feedback
from dependencies import db,cookie_scheme


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[]
    )

@router.post("/submit_post")
async def submit_post(
    current_user: Annotated[User, Depends(get_current_user)],
    new_post: PostIn,
):
    if current_user:
        post_id=upload_post_db(current_user,new_post,db=db)
        return RedirectResponse(f"/posts/{post_id}",status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Redirecting to login page",
            headers={"Location": "/users/login"},
            )

@router.post("/feedback")
async def feedback(current_user: Annotated[User,Depends(get_current_user)],
                   post_id:int,
                   feedback: Feedback=Form(...),
                   session:Session=Depends(cookie_scheme),
):
    if current_user:
        str_feedback=feedback.value
        updatesession(db,session,action=feedback)
        return updateFeedback(current_user,post_id,str_feedback,db=db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can only login to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
@router.put("/post_id/{post_id}")
async def read_a_post(
    token: Annotated[Token, Depends(oauth2_scheme)],
    session: Annotated[Session,Depends(cookie_scheme)],
    post_id:  int,
):
    if token:
        current_user = await get_current_user(token)
        
    else:
        current_user=None
    return get_a_post(db,
                        current_user,
                        post_id)[0]

# not ready
# https://uriyyo-fastapi-pagination.netlify.app/tutorials/cursor-pagination/
@router.get("/{username}")
async def read_own_posts(
    token: Annotated[Token, Depends(oauth2_scheme)],
    username: str,
)->Page[dict]:
    if token:
        current_user = await get_current_user(token)
    else:
        current_user=None
    return paginate(get_posts_by_user(db,
                            current_user,
                            username))