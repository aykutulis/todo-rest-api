from sqlalchemy.orm import Session

from models import UserModel


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not user.verify_password(password):
        return False

    # remove password from user object
    delattr(user, 'password')

    return user
