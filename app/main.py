from fastapi import FastAPI

from app.routers import employees, groups, auth, admin, users
from app.routers import kids

app = FastAPI()

app.include_router(employees.router)
app.include_router(kids.router)
app.include_router(groups.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
