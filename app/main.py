from fastapi import FastAPI

from app.routers import employees, groups, auth, admin, users, parents, database_transfer
from app.routers import kids

app = FastAPI()

app.include_router(employees.router)
app.include_router(kids.router)
app.include_router(groups.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(parents.router)
app.include_router(database_transfer.router)
