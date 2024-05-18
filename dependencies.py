from datetime import datetime, timedelta, timezone,date
from typing import Annotated, Union,Literal
from sql import crud
from sql.schemas import users,posts
#from sql.database import SessionLocal

from sql import crud

from fastapi import Depends,HTTPException, status,Header,Cookie
from fastapi_pagination import Page, paginate
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from fakedb import fake_users_db

from models.users import (
    UserInDB1,UserInDB,TokenData,UserIn,UserOut,UserInpi,UserInDBtag,
    UserInDBpw,Token
    )
from models.posts import PostIn,PostInDB,PostOut

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "ThisIsAWebsiteAboutSavingUrAXX"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token",auto_error=False,)

def get_db():
    db = None #SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    user= crud.get_users(db, username=username)
    if user:
        return UserInDB(**user)
    else:
        return None

def reset_password(db, username, old_password, new_password
):
    user=authenticate_user(db, username,old_password)
    if user:
        userInDBpw=users.UserInDBpw(**user.model_dump(),hashed_password=get_password_hash(new_password))
        return crud.update_user(db,userInDBpw)
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
        user = get_user(fake_users_db, username=token_data.username)
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
    x.update({"user_id":len(db)+1})
    
    new_user_DB=users.UserIn(**x)
    new_user_DB=users.UserInDB(**new_user_DB.model_dump(),certified=False)
    return crud.create_user(db,new_user_DB)

def get_posts_by_user(
        db,
        currentuser: UserInDB,
        username:str
):
    user=get_user(fake_users_db,username)
    if user:
        if not currentuser:
            posts=crud.get_posts(db,user_id=user.user_id,anonymous=False)
        elif currentuser.username==username:
            posts=crud.get_posts(db,user_id=user.user_id,anonymous=True)
        else:
            posts=crud.get_posts(db,user_id=user.user_id,anonymous=False)
        
        return {
            "posts":posts
    }
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
        status_code=status.HTTP_303_SEE_OTHER,
        detail="Redirecting to login page",
        headers={"Location": "/users/login"},
        )
    if username:
        user=get_user(db,username)
        if user:
            dictUserInDB=crud.get_user(db,username)
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
        status_code=status.HTTP_303_SEE_OTHER,
        detail="Redirecting to login page",
        headers={"Location": "/users/login"},
        )
    if username:
        user=get_user(db,username)
        if user:
            person_info=crud.update_user(db,new_info)
            return person_info
        else:
            raise login_exception
    else:
        raise login_exception
    
def show_tags(db,user:UserInDB):
    user_tag=UserInDBtag(**db.get(user.username))
    return user_tag.interested_tag
    
def update_tags(db,
                user:UserInDB,
                new_tag:list):
    dictUserInDB=db.get(user.username)
    UserInDB=users.UserInDBtag(**dictUserInDB)
    dictUserInDB=crud.update_user(db,UserInDB)
    return dictUserInDB

def read_user(db,
              username):
    try:
        user=UserOut(crud.get_users(db,username=username).model_dump())
        return user
    except AttributeError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

def get_a_post(db,
               user:UserInDB,
               post_id: int):
    
    if not user:
        posts=crud.get_posts(db,post_ids=[post_id],anonymous=False)
    else:
        posts=crud.get_posts(db,post_ids=[post_id],user_id=user.user_id)
    
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
        post_date=datetime.now(),
    )
    tfidf=posts.Post_v_tfidfnoId(
        zip(
            ['_'.join(['tfidf',i]) for i in range(0,20)],
            [1/19]*20)
        )
    userDetail=get_user(db,user.username)
    writers_dynamic=posts.Post_v_Writers_dinamicdatanoId(
        **userDetail.model_dump(),
        **post.model_dump()
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

def updatesession(db,
                  session: str,
                  api_key: str,
                  action: Literal["search","click","good","early","impossible"]="search",
                  key_words: str=""):
    return crud.create_userresponsecache(
            db,
            session=session,
            api_key=api_key,
            action=action,
            key_words=key_words
        )