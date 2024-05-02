from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status, Cookie, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from fakedb import fake_users_db

from models.users import Token,User,UserOut,UserInDB
from dependencies import authenticate_user,create_access_token,get_current_user,ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/token", tags=["users"],response_model=UserOut)
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


@router.get("/users/{current_user.username}/", response_model=User, tags=["users"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get("/users/{current_user.username}/posts/", tags=["users"])
async def read_own_posts(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.post("/users/register",response_model=UserOut)
async def create_user(user:UserInDB):
    if user not in fake_users_db:
        fake_users_db.update({user.username:user})
        RedirectResponse('user/login')
    else:
        return {'message':'your username is already used. '}