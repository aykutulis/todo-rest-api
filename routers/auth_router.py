from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from exceptions.CredentialsException import CredentialsException


from schemas import CreateUserSchema
from utils.database_utils import get_db
from utils.auth_utils import authenticate_user, create_access_token, get_current_user
from models import UserModel


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/create")
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException()

    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return current_user
