from datetime import timedelta
from typing import Annotated,Optional

from fastapi import Depends, APIRouter, HTTPException, status, Response,Header
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from fakedb import fake_users_db,fake_post_user_db,fake_posts_db

from models.users import Token,User,UserIn,UserResetPW,UserInpw,UserOut,UserInpi,UserIntag
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
                          get_posts_by_user)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[]
    )


@router.get('/login')
async def login_page():
    return {"message":"Please log in"}

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


@router.get("/{current_user.username}/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@router.post("/{current_user.username}/reset_password",response_model=UserOut)
async def reset_password_post(
    current_user: Annotated[User, Depends(get_current_user)],
    UserDB: UserInpw,
    UserReset: UserResetPW,
):
    user=reset_password(fake_users_db,current_user.username,UserDB.password,UserReset.new_password)
    return user

@router.get("/{current_user.username}/update_personal_info",response_model=UserInpi)
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

@router.post("/{current_user.username}/update_personal_info/submit",response_model=UserInpi)
async def submit_personal_info(
    current_user: Annotated[User, Depends(get_current_user)],
    UserUpdate: UserInpi,
):
    if current_user:
        user=update_personal_info(fake_users_db,current_user.username,UserUpdate)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Redirecting to login page",
            headers={"Location": "/users/login"},
            )

@router.post("/register")
async def create_user(user:UserIn,
                      current_user: User=Depends(get_current_user)):
    if not current_user:
        if user.username not in fake_users_db:
            create_new_user(fake_users_db,user)
            return RedirectResponse('/users/login',status_code=status.HTTP_303_SEE_OTHER)
        else:
            return {'message':'your username is already used.'}
    else:
        return RedirectResponse('/',status_code=status.HTTP_303_SEE_OTHER)

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
async def get_user_page(username: str):
    return read_user(fake_users_db,username)

@router.get("/{username}/posts",tags=["Posts"])
async def read_own_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    username: str,
    max_page_size: int=Header(10),
    page_num:int=Header(1),

):
    return get_posts_by_user(fake_posts_db,
                             fake_post_user_db,
                             current_user,
                             username,
                             max_page_size,
                             page_num)