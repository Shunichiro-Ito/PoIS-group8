from fastapi import APIRouter, Depends,HTTPException,status,Header,Response,Request
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyQuery,APIKeyCookie
from typing import Literal, Annotated
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

from fakedb import fake_posts_db,fake_post_user_db,fake_users_db,fake_feedback_db
from models.users import User
from models.posts import PostIn, Feedback


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[]
    )

query_scheme=APIKeyQuery(name="searchresponse")
cookie_scheme=APIKeyCookie(name="session")

@router.get("/{post_id}")
async def read_post(post_id: int,
                    current_user: Annotated[User,Depends(get_current_user)]):
    return get_a_post(fake_posts_db,fake_post_user_db,fake_users_db,current_user,post_id)

@router.get("/search/{key_words}")
async def search_posts(key_words: str,
                       current_user: Annotated[User,Depends(get_current_user)],
                       cat: Literal["all","post","user"]="all",
                       api_key:str=Depends(query_scheme),
                       session:str=Depends(cookie_scheme)
):
    
    search= searcher('mysql.db')
    search_results=search.query(key_words,cat)
    #use current user to rank the search results

    #update session, key_words in database
    updatesession(session,key_words)

    return {
        "search_results":search_results,
        "api_key":api_key,
        "session":session,
    }

@router.post("/click_post")
async def click_post(post_id:int,
                     session:str=Depends(cookie_scheme),
                     api_key:str=Depends(query_scheme)
):
    updatesession(session,api_key,action="click")
    return RedirectResponse(f"/posts/{post_id}",status_code=status.HTTP_303_SEE_OTHER)

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

@router.post("/feedback")
async def feedback(current_user: Annotated[User,Depends(get_current_user)],
                   post_id:int,
                   feedback: Feedback=Form(...),
                   session:str=Depends(cookie_scheme),
                   api_key:str=Depends(query_scheme)
):
    if current_user:
        str_feedback=feedback.value
        updatesession(session,api_key,action=feedback)
        return updateFeedback(current_user,post_id,str_feedback,fake_feedback_db,fake_posts_db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can only login to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    