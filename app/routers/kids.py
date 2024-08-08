from typing import Annotated

from fastapi import Path, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Kids
from app.schemas.kids import GetKid, CreateKid, UpdateKid

router = APIRouter(
    prefix="/kid",
    tags=["kid"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetKid])
async def read_all_kids(db: db_dependency):
    list_kids = db.query(Kids).all()
    return list_kids


@router.get("/{kid_id}", response_model=GetKid, status_code=status.HTTP_200_OK)
async def read_kid(db: db_dependency, kid_id: int = Path(gt=0)):
    kid_model = db.query(Kids).filter(Kids.id == kid_id).first()
    if kid_model is not None:
        return kid_model
    raise HTTPException(status_code=404, detail='Kid not found.')


@router.post("/create_kid", response_model=GetKid, status_code=status.HTTP_201_CREATED)
async def create_kid(db: db_dependency, kid_request: CreateKid):
    try:
        kid_model = Kids(**kid_request.dict())

        db.add(kid_model)
        db.commit()

        return kid_model
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {e}")


@router.put("/{kid_id}", response_model=GetKid, status_code=status.HTTP_200_OK)
async def update_kid(db: db_dependency, kid_request: UpdateKid, kid_id: int = Path(gt=0)):
    kid_model = db.query(Kids).filter(Kids.id == kid_id).first()
    if kid_model is None:
        raise HTTPException(status_code=404, detail='Kid not found.')

    kid_model.first_name = kid_request.first_name
    kid_model.last_name = kid_request.last_name
    kid_model.father_name = kid_request.father_name
    kid_model.date_of_enrollment = kid_request.date_of_enrollment
    kid_model.gender = kid_request.gender
    kid_model.group_id = kid_request.group_id

    db.add(kid_model)
    db.commit()
    return kid_model


@router.delete("/{kid_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kid(db: db_dependency, kid_id: int = Path(gt=0)):
    kid_model = db.query(Kids).filter(Kids.id == kid_id).first()
    if kid_model is None:
        raise HTTPException(status_code=404, detail='Kid not found.')
    db.query(Kids).filter(Kids.id == kid_id).delete()

    db.commit()
