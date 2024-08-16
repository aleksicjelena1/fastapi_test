from typing import Annotated

from fastapi import Path, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Employees, Groups, Kids
from app.schemas import employees
from app.schemas.groups import GetGroup, CreateGroup, UpdateGroup, UpdateGroupKids

router = APIRouter(
    prefix="/group",
    tags=["group"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetGroup])
async def read_all_groups(db: db_dependency):
    list_groups = []
    db_groups = db.query(Groups).all()
    # dobijamo listu tabele Groups db_groups = [ id=1, name=Bubamarice, id=2, name=Tigrici ...]
    for group in db_groups:
        # group = id = 1, name = Bubamarice
        employee = db.query(Employees).filter(Employees.group_id == group.id).first()
        kids_list = db.query(Kids).filter(Kids.group_id == group.id).all()
        group_schema = GetGroup(
            name=group.name,
            employee=f"{employee.first_name} {employee.last_name}" if employee else "",
            kids=[f"{kid.first_name} {kid.last_name}" for kid in kids_list] if kids_list else []
        )

        list_groups.append(group_schema)

    return list_groups


@router.get("/id/{group_id}", response_model=GetGroup, status_code=status.HTTP_200_OK)
async def read_group_by_id(db: db_dependency, group_id: int = Path(gt=0)):
    db_group = db.query(Groups).filter(Groups.id == group_id).first()

    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    employee = db.query(Employees).filter(Employees.group_id == group_id).first()
    kids_list = db.query(Kids).filter(Kids.group_id == group_id).all()
    group_schema = GetGroup(
        name=db_group.name,
        employee=f"{employee.first_name} {employee.last_name}" if employee else "",
        kids=[f"{kid.first_name} {kid.last_name}" for kid in kids_list] if kids_list else []
    )
    return group_schema


@router.get("/name/{group_name}", response_model=GetGroup, status_code=status.HTTP_200_OK)
async def read_group_by_name(db: db_dependency, group_name: str):
    db_group = db.query(Groups).filter(Groups.name == group_name).first()

    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    employee = db.query(Employees).filter(Employees.group_id == db_group.id).first()
    kids_list = db.query(Kids).filter(Kids.group_id == db_group.id).all()
    group_schema = GetGroup(
        name=db_group.name,
        employee=f"{employee.first_name} {employee.last_name}" if employee else "",
        kids=[f"{kid.first_name} {kid.last_name}" for kid in kids_list] if kids_list else []
    )
    return group_schema


@router.post("/create_group", response_model=GetGroup, status_code=status.HTTP_201_CREATED)
async def create_group(db: db_dependency, group_request: CreateGroup):
    try:
        group_model = Groups(name=group_request.name)
        db.add(group_model)
        db.commit()

        return GetGroup(
            id=group_model.id,
            name=group_model.name
        )

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {e}")


@router.patch("/employee/{group_id}", response_model=GetGroup, status_code=status.HTTP_200_OK)
async def update_group_employee(db: db_dependency, group_id: int, group_request: UpdateGroup):
    group_model = db.query(Groups).filter(Groups.id == group_id).first()
    if group_model is None:
        raise HTTPException(status_code=404, detail='Group not found.')

    employee_model = db.query(Employees).filter(Employees.id == group_request.employee_id).first()

    if employee_model.group_id is not None:
        raise HTTPException(status_code=404, detail='Employee already has a group.')

    employee_model.group_id = group_id

    db.add(employee_model)
    db.commit()

    return GetGroup(
        id=group_model.id,
        name=group_model.name,
        employee=f"{employee_model.first_name} {employee_model.last_name}"
    )


@router.patch("/kids/{group_id}", response_model=GetGroup, status_code=status.HTTP_200_OK)
async def update_group_kid(db: db_dependency, group_id: int, group_request: UpdateGroupKids):
    group_model = db.query(Groups).filter(Groups.id == group_id).first()
    if group_model is None:
        raise HTTPException(status_code=404, detail='Group not found.')
    for kid in group_request.kids_ids:
        kid_model = db.query(Kids).filter(Kids.id == kid).first()

        if kid_model.group_id is not None:
            raise HTTPException(status_code=404, detail='Kid already has a group.')

        kid_model.group_id = group_id

        db.add(kid_model)
    db.commit()

    kid_model = db.query(Kids).filter(Kids.group_id == group_id).all()
    employee = db.query(Employees).filter(Employees.group_id == group_id).first()

    return GetGroup(
        id=group_model.id,
        name=group_model.name,
        employee=f"{employee.first_name} {employee.last_name}",
        kids=[f"{kid.first_name} {kid.last_name}" for kid in kid_model]
    )


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(db: db_dependency, group_id: int = Path(gt=0)):
    group_model = db.query(Groups).filter(Groups.id == group_id).first()
    if group_model is None:
        raise HTTPException(status_code=404, detail='Group not found.')
    db.query(Groups).filter(Groups.id == group_id).delete()

    db.commit()
