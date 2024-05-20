from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from models.users import Token
from urllib.parse import unquote



#import jaccard_sim

from fastapi import (
    Depends,
    FastAPI,
)

from fastapi.security import APIKeyQuery

query_scheme = APIKeyQuery(name="searchresponse")
cookie_scheme = APIKeyQuery(name="session")

from typing import Annotated,Literal
from models.users import User,Session
from sql.database import SQLSession

from dependencies import get_current_user,show_tags,verify_admin,oauth2_scheme,create_session_token

from search.searchengine import searcher
from fakedb import fake_users_db

from routers import posts, users
from fastapi.responses import RedirectResponse
from models.users import Token

app=FastAPI(
    title="Fail Tales",
    description="""
    先輩たちからの経験談。
    """,
    version="0.0.1",
    
)

from dependencies import db

add_pagination(app)

# Not ready
@app.get("/",tags=["Home"])
async def root(token: Annotated[Token, Depends(oauth2_scheme)]):
    if token:
        current_user = await get_current_user(token)
        if current_user:
            if not show_tags(fake_users_db,current_user):

                return RedirectResponse("/users/interest_tags")
            else:
                # AI
                # key: title, value: cal of similarity
                # timeline of posts: db_posts_age - user_age
                # final_recommend_text_list = jaccard_sim.main(current_user)
                # for i in range(5):
                    # key, value = list(candidate_text.items())[i]
                # 当该用户的feedback数量大于10时并且至少有一条评价为good
                return {"user":current_user,"posts":"timeline of posts",}
    else:
        return RedirectResponse("/login")

origins=[
    "http://localhost:3000",
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

@app.post('/neural_network/nnscore',tags=["Search"])
async def train_neural_network(admin:User=Annotated[User,Depends(verify_admin)]):
    Search=searcher()
    return Search.nnscore()

@app.post('/neural_network/train',tags=["Search"])
async def train_neural_network(admin:User=Annotated[User,Depends(verify_admin)]):
    Search=searcher()
    return Search.train()

@app.get('/search/{key_words}',tags=["Search"])
async def search_posts(key_words: str,
                       cat: Literal["all","post","user"]="all",
                       query_token: str=Depends(query_scheme),
):
    from ai.mecab import MecabTokenizer
    key_word_ids=MecabTokenizer().tokenize(key_words)
    Search=searcher()
    urls=Search.query(
            key_words=key_word_ids,
            searchRange=cat,
        )

    return {
        "search result":urls
    }

@app.post('/session_token')
async def create_session(
    current_user: Annotated[User,Depends(get_current_user)],
    key_words: Annotated[str,Depends(unquote)],
    ):
    session_token,query_token=create_session_token(
        db,query=key_words
    )
    RedirectResponse(f"/search/{key_words}")
    return Session(
        session_token=session_token,
        query_token=query_token,
    
    )


#import uvicorn
#if __name__ == "__main__":
#  uvicorn.run("fapi:app", host="localhost", port=8000, reload=True)
