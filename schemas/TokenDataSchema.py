from pydantic import BaseModel


class TokenDataSchema(BaseModel):
    id: int
    email: str
    username: str
