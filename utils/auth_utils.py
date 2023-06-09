from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.Settings import settings
from exceptions.CredentialsException import CredentialsException

from models import UserModel
from schemas import TokenPayloadSchema
from utils.database_utils import db_dependency

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not user.verify_password(password):
        return False

    # remove password from user object
    delattr(user, 'password')

    return user


def create_access_token(user: UserModel, expires_delta: timedelta | None = None):
    to_encode = TokenPayloadSchema(
        id=user.id, email=user.email, username=user.username).dict()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        id: int = payload.get("id")
        email: str = payload.get("email")
        username: str = payload.get("username")
        if username is None or email is None or id is None:
            raise CredentialsException()

        token_data = TokenPayloadSchema(id=id, email=email, username=username)
    except JWTError:
        raise CredentialsException()

    user = db.query(UserModel).filter(UserModel.id == token_data.id).first()

    if user is None:
        raise CredentialsException()

    user = user.__dict__

    del user['password']

    return user

current_user_dependency = Annotated[dict, Depends(get_current_user)]
