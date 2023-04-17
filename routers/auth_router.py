from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from exceptions.CredentialsException import CredentialsException


from schemas import CreateUserSchema, TokenResponseSchema
from utils.database_utils import db_dependency
from utils.auth_utils import authenticate_user, create_access_token, current_user_dependency
from models import UserModel


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/create")
def create_user(user: CreateUserSchema, db: db_dependency):
    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    delattr(new_user, 'password')
    return new_user


@router.post("/token", response_model=TokenResponseSchema)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException()

    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(
    current_user: current_user_dependency
):
    return current_user
