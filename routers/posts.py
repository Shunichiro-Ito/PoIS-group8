from fastapi import APIRouter, Depends,HTTPException,status,Header
from fastapi.responses import RedirectResponse
from typing import Literal, Annotated
from dependencies import (
    oauth2_scheme,
    get_current_user,
    get_posts_by_user,
    get_user,
    get_a_post,
    upload_post_db
)

from fakedb import fake_posts_db,fake_post_user_db,fake_users_db
from models.users import User
from models.posts import PostIn


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[]
    )

@router.get("/{post_id}")
async def read_post(post_id: int,
                    current_user: Annotated[User,Depends(get_current_user)]):
    return get_a_post(fake_posts_db,fake_post_user_db,fake_users_db,current_user,post_id)

@router.get("/{key_words}")
async def search_posts(key_words: str,
                       token: str = Depends(oauth2_scheme)):
    list_posts={}
    return list_posts

@router.post("/submit_post")
async def submit_post(
    current_user: Annotated[User, Depends(get_current_user)],
    new_post: PostIn
):
    if current_user:
        post_id=upload_post_db(current_user,new_post,fake_posts_db,fake_post_user_db)
        return RedirectResponse(f"/posts/{post_id}",status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Redirecting to login page",
            headers={"Location": "/users/login"},
            )

@router.get("/write_post")
async def write_post():
    return {"message":"write post page"}

