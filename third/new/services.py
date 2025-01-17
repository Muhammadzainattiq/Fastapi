from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from model import TokenData, User, UserInDB
from data import fake_users_db

from jose import jwt, JWTError

from passlib.context import CryptoContext

secret_key = "e31af65a516ee407f3a46f0250f6ec0e94f9cf70f15a75ab08a4d693b4028722"

algorithm = "HS256"
access_token_expire_minutes = 30

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptoContext(schemes = ["bcrypt"], deprecated = "auto")

def verify_password(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username:str, password:str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = algorithm)
    return encoded_jwt

async def get_current_user(token:Annotated[str, Depends(oauth_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username = username)
    except JWTError:
            raise credentials_exception
    if token_data.username is None:
        raise credentials_exception
    user = get_user(fake_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail = "inactive user")
    return current_user
