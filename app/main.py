from fastapi import FastAPI, Path

from app.routers import employees

app = FastAPI()

app.include_router(employees.router)
