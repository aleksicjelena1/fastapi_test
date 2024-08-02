from fastapi import FastAPI

from app.routers import employees

app = FastAPI()

app.include_router(employees.router)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}
