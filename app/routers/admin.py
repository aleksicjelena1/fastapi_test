from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Path
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import Users
from app.routers.auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    list_users = db.query(Users).all()
    return list_users


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
