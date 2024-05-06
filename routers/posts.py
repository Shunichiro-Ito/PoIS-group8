from models.posts import PostOut,Post
from fastapi import APIRouter, Depends
from typing import Literal, Annotated
from dependencies import oauth2_scheme,get_current_user,get_posts_by_user,get_user

from fakedb import fake_posts_db,fake_post_user_db
from models.users import User


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[]
    )

@router.get("/{post_id}", response_model=PostOut, response_model_exclude_unset=True)
async def read_post(post_id: Annotated[PostOut, Depends()]):
    return fake_posts_db[post_id]

@router.get("/{key_words}")
async def search_posts(key_words: str,
                       token: str = Depends(oauth2_scheme)):
    list_posts={}
    return list_posts

@router.get("/{checking_user.username}",tags=["Users"])
async def read_own_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    checking_user: Annotated[User, Depends(get_user)],
    max_page_size: int=10,
):
    return get_posts_by_user(fake_posts_db,fake_post_user_db,current_user,checking_user,max_page_size)