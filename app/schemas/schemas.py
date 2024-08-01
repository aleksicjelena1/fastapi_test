from typing import Optional

from pydantic import BaseModel


class EmployeeRequest(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    phone_number: str
    address: str
