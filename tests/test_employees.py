import pytest
from sqlalchemy import text
from fastapi import status

from app.db.models import Employees
from tests.conftest import TestingSessionLocal, engine, client


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


def test_read_all_employees(employees_builder):
    response = client.get("/employee")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_read_one_employees(employees_builder):
    response = client.get("/employee/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == "Test 0"
    assert response.json().get("last_name") == "User 0"
    assert response.json().get("phone_number") == "Number 0"
    assert response.json().get("address") == "Address 0"


def test_read_one_not_found(employees_builder):
    response = client.get("/employee/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not found.'}


def test_create_employee(employees_builder):
    request_data = {
        'first_name': 'Danilo',
        'last_name': 'Dobras',
        'phone_number': '1234567',
        'address': 'Djede Kecmanovica'
    }
    response = client.post('/employee/create_employee', json=request_data)
    assert response.status_code == 201
    assert response.json().get("first_name") == request_data.get("first_name")
    assert response.json().get("last_name") == request_data.get("last_name")
    assert response.json().get("phone_number") == request_data.get("phone_number")
    assert response.json().get("address") == request_data.get("address")


def test_create_employee_failed(employees_builder):
    request_data = {
        'first': 'Danilo',
        'last_name': 'Dobras',
        'phone_number': '1234567',
        'address': 'Djede Kecmanovica'
    }
    response = client.post('/employee/create_employee', json=request_data)
    assert response.status_code == 422


def test_update_employee(employees_builder):
    request_data = {
        'first_name': 'Zeljko',
        'last_name': 'Bozic',
        'phone_number': '123456789',
        'address': 'Nozicko'
    }

    response = client.put('/employee/1', json=request_data)
    assert response.status_code == 200


def test_update_employee_not_found(employees_builder):
    request_data = {
        'first_name': 'Zeljko',
        'last_name': 'Bozic',
        'phone_number': '123456789',
        'address': 'Nozicko'
    }

    response = client.put('/employee/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not found.'}


def test_delete_employee(employees_builder):
    response = client.delete('/employee/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Employees).filter(Employees.id == 1).first()
    assert model is None


def test_delete_employee_not_found(employees_builder):
    response = client.delete('/employee/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not found.'}
