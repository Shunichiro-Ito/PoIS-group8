from models.posts import PostOut,Post
from fastapi import APIRouter, Depends
from typing import Literal, Annotated

from fakedb import fake_posts_db

router = APIRouter()

@router.get("/posts/{post_id}", response_model=PostOut, response_model_exclude_unset=True)
async def read_post(post_id: Annotated[Post, Depends(get_post)]):
    return fake_posts_db[post_id]
