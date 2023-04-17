from sqlalchemy import Boolean, Column, Integer, String, Enum, event
from sqlalchemy.orm import relationship
from utils.database_utils import Base
from passlib.context import CryptContext
import enum

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)

    todos = relationship("TodoModel", back_populates="owner")

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password)


@event.listens_for(UserModel, "before_insert")
def hash_password(mapper, connection, target: UserModel):
    if target.password:
        target.password = bcrypt.hash(target.password)
