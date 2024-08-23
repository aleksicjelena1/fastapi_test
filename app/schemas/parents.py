from typing import Optional

from pydantic import BaseModel, Field


class BaseParent(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    email: str = Field(min_length=5)
    phone_number: str = Field(min_length=3)
    address: str = Field(min_length=5)


class GetParent(BaseParent):
    id: Optional[int] = None
