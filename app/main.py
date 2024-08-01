from fastapi import FastAPI

from app.routers import employees

app = FastAPI()

app.include_router(employees.router)
