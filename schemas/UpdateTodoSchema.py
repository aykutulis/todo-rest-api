from pydantic import BaseModel, Field
from typing import Optional


class UpdateTodoSchema(BaseModel):
    title: Optional[str]
    description: Optional[str] = Field(title="Description", max_length=300)
    priority: Optional[int] = Field(
        gt=0, le=5, description="Priority must be between 1 and 5")
    complete: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy milk",
                "description": "Buy milk from the store",
                "priority": 1,
                "complete": True
            }
        }
