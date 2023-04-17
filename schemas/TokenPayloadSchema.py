from pydantic import BaseModel


class TokenPayloadSchema(BaseModel):
    id: int
    email: str
    username: str
