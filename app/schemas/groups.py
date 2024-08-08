from typing import Optional

from pydantic import BaseModel, Field


class BaseGroup(BaseModel):
    name: str = Field(min_length=3)
    employee: str = Field(min_length=3)
    kids: list[str]


class GetGroup(BaseGroup):
    pass


class CreateGroup(BaseGroup):
    pass


class UpdateGroup(BaseGroup):
    pass
