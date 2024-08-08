from typing import Annotated

from fastapi import Path, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Employees
from app.schemas.employees import GetEmployee, CreateEmployee, UpdateEmployee

router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetEmployee])
async def read_all_employees(db: db_dependency):
    list_employees = db.query(Employees).all()
    return list_employees


@router.get("/{employee_id}", response_model=GetEmployee, status_code=status.HTTP_200_OK)
async def read_employee(db: db_dependency, employee_id: int = Path(gt=0)):
    employee_model = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee_model is not None:
        return employee_model
    raise HTTPException(status_code=404, detail='Employee not found.')


@router.post("/create_employee", response_model=GetEmployee, status_code=status.HTTP_201_CREATED)
async def create_employee(db: db_dependency, employee_request: CreateEmployee):
    try:
        employee_model = Employees(**employee_request.dict())

        db.add(employee_model)
        db.commit()

        return employee_model
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {e}")


@router.put("/{employee_id}", response_model=GetEmployee, status_code=status.HTTP_200_OK)
async def update_employee(db: db_dependency, employee_request: UpdateEmployee, employee_id: int = Path(gt=0)):
    employee_model = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee_model is None:
        raise HTTPException(status_code=404, detail='Employee not found.')

    employee_model.first_name = employee_request.first_name
    employee_model.last_name = employee_request.last_name
    employee_model.phone_number = employee_request.phone_number
    employee_model.address = employee_request.address
    employee_model.group_id = employee_request.group_id

    db.add(employee_model)
    db.commit()
    return employee_model


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(db: db_dependency, employee_id: int = Path(gt=0)):
    employee_model = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee_model is None:
        raise HTTPException(status_code=404, detail='Employee not found.')
    db.query(Employees).filter(Employees.id == employee_id).delete()

    db.commit()
