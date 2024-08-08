from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BaseKid(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    father_name: str = Field(min_length=3)
    date_of_enrollment: str
    gender: str

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str):
        if value not in ["m", "f"]:
            raise ValueError("Gender must be f - female or m - male")
        return value


class GetKid(BaseKid):
    id: Optional[int] = None


class CreateKid(BaseKid):
    pass


class UpdateKid(BaseKid):
    group_id: int = None
