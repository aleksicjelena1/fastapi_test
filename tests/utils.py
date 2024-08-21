import pytest
from sqlalchemy import text

from app.db.models import Groups, Employees, Kids
from tests.conftest import TestingSessionLocal, engine


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
