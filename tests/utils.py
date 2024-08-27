import pytest
from sqlalchemy import text

from app.db.models import Groups, Employees, Kids, Parents
from tests.conftest import TestingSessionLocal, engine, client


@pytest.fixture()
def get_access_token():
    # create data for user
    request_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword",
        "role": "admin"
    }

    client.post('/auth/create_user', json=request_data)
    # get access token
    response = client.post('/auth/token', data={
        "username": request_data["username"],
        "password": request_data["password"]
    })
    response_data = response.json()
    yield response_data.get("access_token")
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def groups_builder():
    db = TestingSessionLocal()
    for i in range(3):
        group = Groups(name=f'Test {i}')
        db.add(group)
    db.commit()
    yield group
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM groups;"))
        connection.commit()


@pytest.fixture
def employees_builder():
    db = TestingSessionLocal()
    for i in range(3):
        employee = Employees(
            first_name=f'Test {i}',
            last_name=f'User {i}',
            phone_number=f'Number {i}',
            address=f'Address {i}'
        )
        db.add(employee)
        db.commit()
    yield employee
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM employees;"))
        connection.commit()


@pytest.fixture
def kids_builder():
    db = TestingSessionLocal()
    for i in range(3):
        kid = Kids(
            first_name=f'Test {i}',
            last_name=f'User {i}',
            father_name=f'Name {i}',
            date_of_enrollment=f'Date {i}',
            gender='m'
        )
        db.add(kid)
        db.commit()
    yield kid
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM kids;"))
        connection.commit()


@pytest.fixture
def parents_builder():
    db = TestingSessionLocal()
    for i in range(3):
        parent = Parents(
            first_name=f'Test {i}',
            last_name=f'User {i}',
            email=f'test {i}',
            phone_number=f'Number {i}',
            address=f'Address {i}'
        )
        db.add(parent)
        db.commit()
    yield parent
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM parents;"))
        connection.commit()
