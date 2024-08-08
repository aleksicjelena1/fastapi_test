from fastapi import FastAPI

from app.routers import employees, groups
from app.routers import kids

app = FastAPI()

app.include_router(employees.router)
app.include_router(kids.router)
app.include_router(groups.router)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}
