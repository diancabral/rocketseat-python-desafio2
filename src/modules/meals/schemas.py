from pydantic import BaseModel, Field


class CreateMealBody(BaseModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=24)
