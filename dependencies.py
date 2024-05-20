from datetime import datetime, timedelta, timezone,date
from typing import Annotated, Optional, Union,Literal
from sql import crud
from sql.schemas import users,posts,nodes
#from sql.database import SessionLocal

from sql import crud
from search import nn

from fastapi import Depends,HTTPException, status,Header,Cookie
from fastapi_pagination import Page, paginate
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from fakedb import fake_users_db

from fastapi.security import APIKeyQuery, APIKeyCookie

cookie_scheme = APIKeyCookie(name="Session",auto_error=False)

from models.users import (
    UserInDB1,UserInDB,TokenData,UserIn,UserOut,UserInpi,UserInDBtag,
    UserInDBpw,Token,Session
    )
from models.posts import PostIn,PostInDB,PostOut,DisplayPost
from fastapi.security import APIKeyCookie, APIKeyQuery

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "ThisIsAWebsiteAboutSavingUrAXX"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token",auto_error=False,)
session_scheme = APIKeyCookie(name="session",description="User's query",auto_error=False,)
from sql.database import SQLSession
db=SQLSession()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    try:
        user= crud.get_users(db, username=username)
        if user:
            return UserInDB(**user)
        else:
            return None
    except:
        return None

def reset_password(db, username, old_password, new_password
):
    user=authenticate_user(db, username,old_password)
    if user:
        user.hashed_password=get_password_hash(new_password)
        userInDBpw=users.UserInDBpw(**user.model_dump())
        output=crud.update_user(db,userInDBpw)['user']
        return UserOut(**output)
        return UserOut(**output.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: Annotated[Token, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = get_user(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    else:
        raise credentials_exception

def create_new_user(
        db,
        new_user: UserIn
):
    x=vars(new_user)
    x.update({"hashed_password":get_password_hash(new_user.password)})
    x.update({"user_id":0})
    
    new_user_DB=users.UserIn(**x)
    new_user_DB=users.UserInDB(
        **new_user_DB.model_dump(),
        certified=False,
        hashed_password=get_password_hash(new_user.password),
        user_id=0,
    )
    output=crud.create_user(db,new_user_DB)
    user,url=output['user'],output['url']
    return UserOut(**user.model_dump())

def get_posts_by_user(
        db,
        currentuser: UserInDB,
        username:str
):
    user=get_user(fake_users_db,username)
    if user:
        if not currentuser:
            posts=crud.get_posts(db,user_id=user.user_id,anonymousIncluded=False)
        elif currentuser.username==username:
            posts=crud.get_posts(db,user_id=user.user_id,anonymousIncluded=True)
        else:
            posts=crud.get_posts(db,user_id=user.user_id,anonymousIncluded=False)
        
        return posts
    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

def get_personal_info(
        db,
        username,
):
    login_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not login",
        )
    if username:
        user=get_user(db,username)
        if user:
            dictUserInDB=crud.get_users(db,username=username)
            return UserInpi(**dictUserInDB)
        else:
            raise login_exception
    else:
        raise login_exception

def update_personal_info(db,
                         username,
                         new_info: users.UserInDBchar
):
    login_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not login",
        )
    if username:
        user=get_user(db,username)
        if user:
            print(new_info)
            person_info=crud.update_user(db,new_info)['user']
            return person_info
        else:
            raise login_exception
    else:
        raise login_exception
    
def show_tags(db,user:UserInDB):
    userDB=crud.get_users(db,username=user.username)
    user_tag=crud.get_tags(db,user_id=userDB['user_id'])
    #user_tag=crud.get_tags(db,user_id=userDB.user_id)
    #user_tag=UserInDBtag(**userDB.model_dump())
    return user_tag
    
def get_all_tags(db):
    return crud.get_categories(db)

def update_tags(db,
                user:UserInDB,
                new_tag:list[int]
                ):
    old_interest_tags=crud.get_tags(db,username=user.username)

    userTag=users.UserInDBtag(
                        user_id=user.user_id,
                        username=user.username,
                        interested_tag=new_tag,
                        displayed_name=user.displayed_name,
                        )
    output=crud.update_user(db,user=userTag)
    return output

def read_user(db,
              username,
              current_user: Union[UserInDB,None]=None,
):
    NotExistException=HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
    try:
        user=crud.get_users(db,username=username)
        if user:
            if current_user:
                if current_user.username==username:
                    user=UserInDB(**user)
                    #user=UserInDB(**user.model_dump())
                else:
                    user=UserOut(**user)
                    #user=UserOut(**user.model_dump())
            else:
                user=UserOut(**user)
                #user=UserOut(**user.model_dump())
        
            return user
        else:
            raise NotExistException
    except AttributeError:
        raise NotExistException

def get_a_post(db,
               post_id: int,
               user:Optional[UserInDB]=None,
               
):
    if not user:
        posts=crud.get_posts(db,post_ids=[post_id],anonymousIncluded=False)
    else:
        posts=crud.get_posts(db,post_ids=[post_id],username=user.username)
    if len(posts)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    else:
        return posts

def verify_token(token: str = Header(None), session_token: str = Cookie(None)):
    if token or session_token:
        return True
    else:
        return False
    
def show_users(db):
    users=crud.get_users(db,all=True)
    return users

def certify_user(db,
                username: str,
                certify: bool):
    user=get_user(db,username)
    if user:
        newUpdate=users.UserCert(**user.model_dump())
        newUpdate.certified=certify
        output=crud.update_user(db,newUpdate)
        return output
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
def verify_admin(db,
                user: UserInDB,
):
    creditialException=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not admin",
        headers={"Date":datetime.now()},
    )
    admin=crud.get_admin(db,user.username)
    if admin:
        return UserInDB(**admin)
    else:
        raise creditialException

def upload_post_db(
        user: UserInDB,
        new_post: PostIn,
        db
):
    post=posts.PostInDB(
        **new_post.model_dump(),
        post_id=0,
        username=user.username,
        user_id=user.user_id,
        post_date=datetime.now(),
    )
    dict_tfidf={key:value for key,value in zip(
        ['_'.join(['tfidf',str(i)]) for i in range(0,20)],
        [1/19]*20)}
    tfidf=posts.Post_v_tfidfnoId(
        **dict_tfidf
        )
    userDetail=get_user(db,user.username)
    dictuserDetail=userDetail.model_dump()
    dictuserDetail.pop('user_id')
    tag_id=post.tag_id[0]
    dictPost=post.model_dump()
    dictPost.pop('tag_id')
    dictPost.update({'category_id':tag_id})
    writers_dynamic=posts.Post_v_Writers_dinamicdatanoId(
        **dictuserDetail,
        **dictPost
    )
    output=crud.create_post(
        db,
        post=post,
        writers_dynamic=writers_dynamic,
        tfidf=tfidf,
    )
    return output

def updateFeedback(current_user: UserInDB,
                   post_id: int,
                   feedback: str,
                   db
):
    current=crud.get_feedback(db,user_id=current_user.user_id,post_id=post_id)
    if current and current.feedback==feedback:
        pt,fb=crud.update_post(
            db,
            post_id=post_id,
            feedback=None,
            user_id=current_user.user_id
        )
    else:
        pt,fb=crud.update_post(
            db,
            post_id=post_id,
            feedback=feedback,
            user_id=current_user.user_id
        )

    return posts.PostOut(**pt),

def create_session_token(db,
                         query,
                         username
                     ):
    from uuid import uuid4
    from time import time

    sessionvalue=f'{uuid4().hex}-{str(int(time()))}'
    querys=f'{username}={query}'

    updatesession(
        db=db,
        session=sessionvalue,
        key_words=query,
        action="search"
    )

    return sessionvalue,querys

def updatesession(db,
                  session: str,
                  action: Literal["search","click","good","early","impossible"]="search",
                  selectedurl: Optional[str]=None,
                  key_words: str=""):
    if action=="search":
        return crud.create_userresponsecache(
            db,
            userresponsecache=nodes.userResponseCacheIn(
                sessionvalue=session,
                querys=key_words,
                selectedurl=None,
                action=action
            )
        )
    else:
        search_info=crud.get_userresponsecache(db,session=session)
        urlid=crud.get_urls(db,url=selectedurl)
        print(f"urlid: {urlid}")
        if urlid:
            urlid=urlid[0]['url_id']
        else:
            return "Error: url not found"
        urlids=[i['url_id'] for i in crud.get_urls(db)]
        if search_info:
            key_words=search_info['querys']
            from ai import mecab
            mecabTokenizer=mecab.MecabTokenizer()
            wordids=mecabTokenizer.tokenize(key_words)
            result=nn.searchnet().trainquery(
                        wordids=wordids,
                        urlids=urlids,
                        selectedurl=urlid,
                        action=action
                    )
            return result,crud.create_userresponsecache(
                    db,
                    userresponsecache=nodes.userResponseCacheIn(
                        sessionvalue=session,
                        querys=key_words,
                        selectedurl=selectedurl,
                        action=action
                    )
                )
        else:
            print(f"no search_info")

def get_display_posts_by_urls(urls):
    
    posts=crud.get_posts(db,post_ids=[i['post_id'] for i in urls
                                      if i['category']=='post'])
    
    user_info=crud.get_users(db,post_ids=[i['post_id'] for i in urls])

    displayed_posts_dict=zip(posts,user_info,urls)
    displayed_posts=[]
    for i,j,k in displayed_posts_dict:
        if i['anonymous']:
            j['user_id']=None
            j['displayed_name']=None
            j['username']=None
        k.pop('user_id')
        k.pop('post_id')
        displayed_posts.append(DisplayPost(
            **i,
            **j,
            **k
        ))
    print(f"length of post{len(posts)}, length of users{len(user_info)}, length of urls{len(urls)}, length of displayed_posts{len(displayed_posts)}")
    return displayed_posts