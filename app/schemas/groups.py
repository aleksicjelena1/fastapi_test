from typing import Optional

from pydantic import BaseModel, Field


class BaseGroup(BaseModel):
    name: str = Field(min_length=3)
    employee: str = None
    kids: list[str] = None


class GetGroup(BaseGroup):
    id: int


class CreateGroup(BaseModel):
    name: str = Field(min_length=3)


class UpdateGroup(BaseModel):
    employee_id: int


class UpdateGroupKids(BaseModel):
    kids_ids: list[int]
