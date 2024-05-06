from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fakedb import fake_users_db

from fastapi import Depends,HTTPException, status,Header,Cookie
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.users import UserInDB,TokenData,UserIn,UserOut,UserInpi,UserInDBchar,UserInDBtag

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "ThisIsAWebsiteAboutSavingUrAXX"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token",auto_error=False)

def verify_password(plain_password, hashed_password):
    print(plain_password,hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def reset_password(db, username, old_password, new_password
):
    user=authenticate_user(db, username,old_password)
    if user:
        db.update({user.username:{
            "hashed_password":get_password_hash(new_password)
        }})

        return UserOut(**vars(user))
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

def verify_token(token: str = Header(None), session_token: str = Cookie(None)):
    if token or session_token:
        return True
    else:
        return False

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
        user = get_user(fake_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    else:
        return None

def create_new_user(
        db,
        new_user: UserIn
):
    x=vars(new_user)
    x.update({"hashed_password":get_password_hash(new_user.password)})
    new_user_DB=UserInDB(**x)
    db.update({new_user.username:vars(new_user_DB)})
    return 

def get_posts_by_user(
        post_db, 
        post_user_db,
        currentuser: UserInDB,
        user:UserInDB,
        max_page_size: int
):
    if currentuser==user:
        post_ids=[post_user_db[i] for i in post_user_db if post_user_db[i]["username"==user.username]]
        return [post_db[j] for j in post_ids][:max_page_size]
    else:
        post_ids=[post_user_db[i] for i in post_user_db if post_user_db[i]["username"==user.username]]
        return [post_db[j] for j in post_ids if post_db[j]["anonymous"]][:max_page_size]

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
            dictUserInDB=db.get(user.username)
            return UserInpi(**dictUserInDB)
        else:
            raise login_exception
    else:
        raise login_exception

def update_personal_info(db,
                         username,
                         new_info: UserInpi
):
    login_exception=HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        detail="Redirecting to login page",
        headers={"Location": "/users/login"},
        )
    if username:
        user=get_user(db,username)
        if user:
            dictUserInDB=db.get(user.username)
            dictUserInDB.update(vars(new_info))
            person_info=UserInpi(**dictUserInDB)
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
    dictUserInDB.update({"interested_tag": new_tag})
    return dictUserInDB["interested_tag"]

def read_user(db,
              username):
    try:
        user=UserOut(**db.get(username))
        return user
    except AttributeError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )