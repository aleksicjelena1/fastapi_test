from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel

from app.schemas.schemas import EmployeeRequest

app = FastAPI()


class Employee:
    id: int
    first_name: str
    last_name: str
    phone_number: str
    address: str

    def __init__(self, id, first_name, last_name, phone_number, address):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address


class Kids:
    id: int
    first_name: str
    last_name: str
    date_of_starting: datetime

    def __init__(self, id, first_name, last_name, date_of_starting):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_starting = date_of_starting


class KidsRequest(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    date_of_starting: datetime



EMPLOYEES = [
    Employee(1, 'Stefan', 'Cosic', '065111222', 'Milosa Obilica'),
    Employee(2, 'Zeljana', 'Timarac', '065222333', 'Rajka Bosnica'),
    Employee(3, 'Jelena', 'Aleksic', '065333444', 'Milesevska')
]


@app.get("/employees")
async def read_all_employees():
    return EMPLOYEES


@app.get("/{employee_id}")
async def read_employee(employee_id: int = Path(gt=0)):
    for employee in EMPLOYEES:
        if employee.id == employee_id:
            return employee


@app.post("/create_employee")
async def create_employee(employee_request: EmployeeRequest):
    new_employee = Employee(**employee_request.dict())
    EMPLOYEES.append(find_employee_id(new_employee))


def find_employee_id(employee: Employee):
    employee.id = 1 if len(EMPLOYEES) == 0 else EMPLOYEES[-1].id + 1
    return employee


@app.put("/update_employee")
async def update_employee(employee: EmployeeRequest):
    for i in range(len(EMPLOYEES)):
        if EMPLOYEES[i].id == employee.id:
            EMPLOYEES[i] = employee


@app.delete("/delete_employee")
async def delete_employee(employee_id: int):
    for i in range(len(EMPLOYEES)):
        if EMPLOYEES[i].id == employee_id:
            EMPLOYEES.pop()
            break
