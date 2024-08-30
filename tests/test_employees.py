from fastapi import status

from app.db.models import Employees
from tests.conftest import TestingSessionLocal, client
from tests.utils import employees_builder, get_access_token


def test_read_all_employees(employees_builder, get_access_token):
    response = client.get("/employee", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_read_all_employees_not_authorized(employees_builder):
    response = client.get("/employee")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_employee(employees_builder, get_access_token):
    response = client.get("/employee/1", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == "Test 0"
    assert response.json().get("last_name") == "User 0"
    assert response.json().get("phone_number") == "Number 0"
    assert response.json().get("address") == "Address 0"


def test_read_employee_not_authorized(employees_builder):
    response = client.get("/employee/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_one_not_found(employees_builder, get_access_token):
    response = client.get("/employee/999", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not found.'}


def test_read_one_not_found_not_authorized(employees_builder):
    response = client.get("/employee/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_employee(employees_builder, get_access_token):
    request_data = {
        'first_name': 'Danilo',
        'last_name': 'Dobras',
        'phone_number': '1234567',
        'address': 'Djede Kecmanovica'
    }
    response = client.post('/employee/create_employee', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 201
    assert response.json().get("first_name") == request_data.get("first_name")
    assert response.json().get("last_name") == request_data.get("last_name")
    assert response.json().get("phone_number") == request_data.get("phone_number")
    assert response.json().get("address") == request_data.get("address")


def test_create_employee_not_authorized(employees_builder):
    response = client.post("/employee/create_employee")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_employee_failed(employees_builder, get_access_token):
    request_data = {
        'first': 'Danilo',
        'last_name': 'Dobras',
        'phone_number': '1234567',
        'address': 'Djede Kecmanovica'
    }
    response = client.post('/employee/create_employee', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 422


def test_create_employee_failed_not_authorized(employees_builder):
    response = client.post("/employee/create_employee")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_employee(employees_builder, get_access_token):
    request_data = {
        'first_name': 'Zeljko',
        'last_name': 'Bozic',
        'phone_number': '123456789',
        'address': 'Nozicko'
    }

    response = client.put('/employee/1', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200


def test_update_employee_not_authorized(employees_builder):
    response = client.put("/employee/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_employee_not_found(employees_builder, get_access_token):
    request_data = {
        'first_name': 'Zeljko',
        'last_name': 'Bozic',
        'phone_number': '123456789',
        'address': 'Nozicko'
    }

    response = client.put('/employee/999', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not found.'}


def test_update_employee_not_found_not_authorized(employees_builder):
    response = client.put("/employee/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_employee(employees_builder, get_access_token):
    response = client.delete('/employee/1', headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Employees).filter(Employees.id == 1).first()
    assert model is None


def test_delete_employee_not_authorized(employees_builder):
    response = client.delete("/employee/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_employee_not_found(employees_builder, get_access_token):
    response = client.delete('/employee/999', headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not found.'}


def test_delete_employee_not_found_not_authorized(employees_builder):
    response = client.delete("/employee/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
