from pydantic import BaseModel, Field
from typing import Optional


class CreateTodoSchema(BaseModel):
    title: str
    description: Optional[str] = Field(title="Description", max_length=300)
    priority: int = Field(
        gt=0, le=5, description="Priority must be between 1 and 5")
    complete: bool

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy milk",
                "description": "Buy milk from the store",
                "priority": 1,
                "complete": False
            }
        }
