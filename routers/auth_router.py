from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta


from schemas import CreateUserSchema
from utils.database_utils import get_db
from utils.auth_utils import authenticate_user, create_access_token
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
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
