from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import CreateUserSchema
from utils.database import get_db
from models import UserModel


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("")
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
