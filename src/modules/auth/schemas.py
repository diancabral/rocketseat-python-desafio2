from pydantic import BaseModel, Field


class AuthLoginBody(BaseModel):
    username: str = Field(max_length=24)
    password: str = Field(max_length=24)
