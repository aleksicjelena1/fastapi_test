from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Parents
from app.routers.auth import get_current_user
from app.schemas.parents import GetParent

router = APIRouter(
    prefix="/parent",
    tags=["parent"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetParent])
async def read_all_parents(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    list_parents = db.query(Parents).all()
    return list_parents
