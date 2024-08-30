from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Parents
from app.routers.auth import get_current_user
from app.schemas.parents import GetParent, CreateParent, UpdateParent

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/parent",
    tags=["parent"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetParent])
async def read_all_parents(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    list_parents = db.query(Parents).all()
    return list_parents


@router.get("/{parent_id}", response_model=GetParent, status_code=status.HTTP_200_OK)
async def read_parent(user: user_dependency, db: db_dependency, parent_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')

    parent_model = db.query(Parents).filter(Parents.id == parent_id).first()
    if parent_model is not None:
        return parent_model
    raise HTTPException(status_code=404, detail='Parent not found.')


@router.post("/create_parent", response_model=GetParent, status_code=status.HTTP_201_CREATED)
async def create_parent(user: user_dependency, db: db_dependency, parent_request: CreateParent):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed.')
        parent_model = Parents(**parent_request.dict())

        db.add(parent_model)
        db.commit()

        return parent_model
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {e}")


@router.put("/{parent_id}", response_model=GetParent, status_code=status.HTTP_200_OK)
async def update_parent(user: user_dependency, db: db_dependency, parent_request: UpdateParent, parent_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')

    parent_model = db.query(Parents).filter(Parents.id == parent_id).first()
    if parent_model is None:
        raise HTTPException(status_code=404, detail='Parent not found.')

    parent_model.first_name = parent_request.first_name
    parent_model.last_name = parent_request.last_name
    parent_model.email = parent_request.email
    parent_model.phone_number = parent_request.phone_number
    parent_model.address = parent_request.address
    parent_model.kid_id = parent_request.kid_id

    db.add(parent_model)
    db.commit()
    return parent_model


@router.delete("/{parent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parent(user: user_dependency, db: db_dependency, parent_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')

    parent_model = db.query(Parents).filter(Parents.id == parent_id).first()
    if parent_model is None:
        raise HTTPException(status_code=404, detail='Parent not found.')
    db.query(Parents).filter(Parents.id == parent_id).delete()

    db.commit()
