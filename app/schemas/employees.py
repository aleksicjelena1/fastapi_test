from typing import Optional, List

from pydantic import BaseModel, Field


class BaseEmployee(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    phone_number: str
    address: str


class GetEmployee(BaseEmployee):
    id: Optional[int] = None


class CreateEmployee(BaseEmployee):
    pass


class UpdateEmployee(BaseEmployee):
    pass
