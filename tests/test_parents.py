from starlette import status

from app.db.models import Parents
from tests.conftest import client, TestingSessionLocal
from tests.utils import parents_builder, get_access_token


def test_read_all_parents(parents_builder, get_access_token):
    response = client.get("/parent", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_read_all_parents_not_authorized(parents_builder):
    response = client.get("/parent")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_one_parent(parents_builder, get_access_token):
    response = client.get("/parent/1", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == "Test 0"
    assert response.json().get("last_name") == "User 0"
    assert response.json().get("email") == "test 0"
    assert response.json().get("phone_number") == "Number 0"
    assert response.json().get("address") == "Address 0"


def test_read_parent_not_authorized(parents_builder):
    response = client.get("/parent/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_one_not_found(parents_builder, get_access_token):
    response = client.get("/parent/999", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Parent not found.'}


def test_read_one_not_found_not_authorized(parents_builder):
    response = client.get("/parent/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_employee(parents_builder, get_access_token):
    request_data = {
        'first_name': 'Irena',
        'last_name': 'Vukojevic',
        'email': 'saldo@gamil.com',
        'phone_number': '065875373',
        'address': 'Duska Koscice'
    }
    response = client.post('/parent/create_parent', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 201
    assert response.json().get("first_name") == request_data.get("first_name")
    assert response.json().get("last_name") == request_data.get("last_name")
    assert response.json().get("email") == request_data.get("email")
    assert response.json().get("phone_number") == request_data.get("phone_number")
    assert response.json().get("address") == request_data.get("address")


def test_create_parent_not_authorized(parents_builder):
    response = client.post("/parent/create_parent")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_parent_failed(parents_builder, get_access_token):
    request_data = {
        'first_namee': 'Irena',
        'last_name': 'Vukojevic',
        'email': 'saldo@gamil.com',
        'phone_number': '065875373',
        'address': 'Duska Koscice'
    }
    response = client.post('/parent/create_parent', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 422


def test_create_parent_failed_not_authorized(parents_builder):
    response = client.post("/parent/create_parent")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_parent(parents_builder, get_access_token):
    request_data = {
        'first_name': 'Jelena',
        'last_name': 'Javor',
        'email': 'email@gmail.com',
        'phone_number': '123456789',
        'address': 'Borik'
    }

    response = client.put('/parent/1', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200


def test_update_employee_not_authorized(parents_builder):
    response = client.put("/parent/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_employee_not_found(parents_builder, get_access_token):
    request_data = {
        'first_name': 'Jelena',
        'last_name': 'Javor',
        'email': 'email@gmail.com',
        'phone_number': '123456789',
        'address': 'Borik'
    }

    response = client.put('/parent/999', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Parent not found.'}


def test_update_parent_not_found_not_authorized(parents_builder):
    response = client.put("/parent/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_parent(parents_builder, get_access_token):
    response = client.delete('/parent/1', headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Parents).filter(Parents.id == 1).first()
    assert model is None


def test_delete_parent_not_authorized(parents_builder):
    response = client.delete("/parent/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_parent_not_found(parents_builder, get_access_token):
    response = client.delete('/parent/999', headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Parent not found.'}


def test_delete_employee_not_found_not_authorized(parents_builder):
    response = client.delete("/parent/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
