from typing import Annotated

from fastapi import Path, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Employees, Groups
from app.schemas.employees import GetEmployee, CreateEmployee, UpdateEmployee
from app.schemas.groups import GetGroup

router = APIRouter(
    prefix="/group",
    tags=["group"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetGroup])
async def read_all_groups(db: db_dependency):
    list_groups = []
    db_groups = db.query(Groups).all()
    for group in db_groups:
        employee = db.query(Employees).filter(Employees.id == group.employee_id).first()
        group_schema = GetGroup(
            name=group.name,
            employee=f"{employee.first_name} {employee.last_name}",
            kids=[]
        )

        list_groups.append(group_schema)

    return list_groups
