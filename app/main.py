from fastapi import FastAPI

from app.routers import employees
from app.routers import kids

app = FastAPI()

app.include_router(employees.router)
app.include_router(kids.router)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}
