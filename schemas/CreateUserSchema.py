from pydantic import BaseModel
from typing import Optional

from models.UserModel import UserRole


class CreateUserSchema(BaseModel):
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: str
    role: Optional[UserRole]
