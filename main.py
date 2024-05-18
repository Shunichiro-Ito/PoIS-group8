from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from models.users import Token

from fastapi import (
    Depends,
    FastAPI,
)

from fastapi.security import APIKeyQuery

query_scheme = APIKeyQuery(name="searchresponse")
cookie_scheme = APIKeyQuery(name="session")

from typing import Annotated,Literal
from models.users import User
from dependencies import get_current_user,show_tags,verify_admin,oauth2_scheme

from search.searchengine import searcher
from fakedb import fake_users_db

from routers import posts, users

app=FastAPI(
    title="失敗なし",
    description="""
    先輩たちからの経験談。
    """,
    version="0.0.1",
    
)

add_pagination(app)

# Not ready
@app.get("/",tags=["home"])
async def root(token: Annotated[Token, Depends(oauth2_scheme)]):
    if token:
        current_user=User(get_current_user())
        if current_user:
            if not show_tags(fake_users_db,current_user):
                return RedirectResponse("/users/interest_tags")
            else:
                return {"user":current_user,"posts":"timeline of posts",}
    else:
        return RedirectResponse("/login")

origins=[
    "http://localhost:3306",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(posts.router)


@app.get('/login')
async def login_page():
    return {"message":"login page"}

@app.post('/neural_network/nnscore')
async def train_neural_network(admin:User=Annotated[User,Depends(verify_admin)]):
    Search=searcher()
    return Search.nnscore()

@app.post('/neural_network/train')
async def train_neural_network(admin:User=Annotated[User,Depends(verify_admin)]):
    Search=searcher()
    return Search.train()

@app.get('/search/{key_words}')
async def search_posts(key_words: str,
                       current_user: Annotated[User,Depends(get_current_user)],
                       cat: Literal["all","post","user"]="all",
                       api_key:str=Depends(query_scheme),
                       session:str=Depends(cookie_scheme)
):
    Search=searcher()
    Search.query()
    return Search.search(key_words,cat)



#import uvicorn
#if __name__ == "__main__":
#  uvicorn.run("fapi:app", host="0.0.0.0", port=8000, reload=True)
