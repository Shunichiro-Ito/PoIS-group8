from datetime import timedelta,datetime
from typing import Annotated,Optional

from fastapi import Depends, APIRouter, HTTPException, status, Response,Header,Body,Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi_pagination import paginate
from fastapi_pagination.links import Page
from fastapi_pagination.cursor import CursorPage

#from sqlalchemy.orm import Session
#from sql.database import SessionLocal
#from sql import crud

from fakedb import fake_users_db,fake_post_user_db,fake_posts_db,fake_admin_db

from models.users import Token,User,UserIn,UserResetPW,UserInpw,UserOut,UserInpi,UserIntag,UserInDB
from dependencies import (authenticate_user,
                          create_access_token,
                          get_current_user,
                          ACCESS_TOKEN_EXPIRE_MINUTES,
                          create_new_user,
                          reset_password,
                          get_personal_info,
                          update_personal_info,
                          show_tags,
                          update_tags,
                          read_user,
                          oauth2_scheme,
                          get_posts_by_user,
                          verify_admin,
                          show_users,
                          certify_user)

from sql.database import SQLSession

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[]
    )

db=SQLSession()

@router.post("/token",response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/reset_password",response_model=UserOut)
async def reset_password_post(
    current_user: Annotated[User, Depends(get_current_user)],
    UserDB: UserInpw,
    UserReset: UserResetPW,
):
    user=reset_password(fake_users_db,current_user.username,UserDB.password,UserReset.new_password)
    return UserOut(**user.model_dump())

@router.get("/update_personal_info",response_model=UserInpi)
async def personal_info(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user:
        user=get_personal_info(fake_users_db,current_user.username)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Redirecting to login page",
            headers={"Location": "/users/login"},
            )

@router.post("/update_personal_info/submit",response_model=UserInpi)
async def submit_personal_info(
    current_user: Annotated[User, Depends(get_current_user)],
    UserUpdate: UserInpi,
):
    if current_user:
        user=update_personal_info(fake_users_db,current_user.username,UserUpdate)
        output=UserInpi(**user)
        #output=UserInpi(**user.model_dump())
        return output
    else:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Redirecting to login page",
            headers={"Location": "/users/login"},
            )

@router.get("/")
async def users_page(current_user: User=Depends(get_current_user))->Page[UserInDB]:
    if current_user:
        if verify_admin(db,current_user):
            return paginate(show_users(fake_users_db))
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="Page not found.",
                                headers={"WWW-Authenticate": "Bearer"})
    else:
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                            detail="Redirecting to login page",
                            headers={"Location": "/users/login"})
    
@router.post("/certify")
async def certify_submit(certifying_username: str=Body(...),
                         certify: bool=Body(...),
                         current_user: User=Depends(get_current_user)):
    if verify_admin(fake_admin_db,current_user):
        certify_user(fake_users_db,certifying_username,certify)
        if certify:
            return {"message":"certified"}
        else:
            return {"message":"uncertified"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not admin",
            headers={"Date":datetime.now(),
                     "WWW-Authenticate": "Bearer"},
        )

@router.post("/register")
async def create_user(user:UserIn):
    if user.username not in fake_users_db:
        create_new_user(fake_users_db,user)
        return RedirectResponse('/login',status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {'message':'your username is already used.'}

@router.get("/interest_tags")
async def get_user_tag(current_user: User=Depends(get_current_user)):
    return show_tags(fake_users_db,current_user)

@router.post("/interest_tags/submit")
async def update_user_tag_submit(tags:UserIntag,
                          current_user: User=Depends(get_current_user)):
    update_tags(fake_users_db,current_user,tags)
    return RedirectResponse('/',status_code=status.HTTP_303_SEE_OTHER)

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    if current_user:
        return RedirectResponse(f"/users/{current_user.username}")
    else:
        return RedirectResponse("/users/login")

@router.get("/{username}")
async def get_user_page(username: str,
                        token:Annotated[Token, Depends(oauth2_scheme)]):
    if token:
        current_user = await get_current_user(token)
        return read_user(db,username,current_user)
    else:
        return read_user(db,username)

