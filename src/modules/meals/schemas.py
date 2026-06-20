from pydantic import BaseModel, ConfigDict, Field


class CreateMealBody(BaseModel):
    name: str = Field(max_length=24)
    description: str = Field(max_length=100)
    is_diet: bool


class EditMealBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, max_length=24)
    description: str | None = Field(default=None, max_length=100)
    is_diet: bool | None = None
