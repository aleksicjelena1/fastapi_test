from fastapi import FastAPI, APIRouter
from typing import List

from app.db.sqlite_postgres_migration import transfer_table

router = APIRouter(
    prefix="/transfer",
    tags=["transfer"]
)


@router.post("/transfer/")
async def transfer_data(tables: List[str]):
    for table in tables:
        transfer_table(table)
    return {"message": "Data transfer complete."}
