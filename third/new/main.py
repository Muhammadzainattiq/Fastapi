from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import Token, User
from data import fake_users_db

from services import authenticate_user, create_access_token, get_current_active_user, access_token_expire_minutes

app = FastAPI()

@app.post("token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depnds()]
) -> Token:
    user = authenticate_user(fake_users_db,
                             form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes = access_token_expire_minutes)
    access_token = create_access_token(
        data = {"sun": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token = access_token, token_tupe = "bearer")


@app.get('users/me', response_model = User)
async def read_users_me(current_user: Annotated[User, get_current_active_user]):
    return current_user

