from fastapi import status

from app.db.models import Kids
from tests.conftest import TestingSessionLocal, engine, client
from tests.utils import kids_builder

def test_read_all_kids(kids_builder):
    response = client.get("/kid")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_read_one_kids(kids_builder):
    response = client.get("/kid/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("first_name") == "Test 0"
    assert response.json().get("last_name") == "User 0"
    assert response.json().get("father_name") == "Name 0"
    assert response.json().get("date_of_enrollment") == "Date 0"
    assert response.json().get("gender") == "m"


def test_read_one_not_found(kids_builder):
    response = client.get("/kid/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Kid not found.'}


def test_create_kid(kids_builder):
    request_data = {
        'first_name': 'Katarina',
        'last_name': 'Kovacic',
        'father_name': 'Milan',
        'date_of_enrollment': '30-September-2020',
        'gender': 'f'
    }
    response = client.post('/kid/create_kid', json=request_data)
    assert response.status_code == 201
    assert response.json().get("first_name") == request_data.get("first_name")
    assert response.json().get("last_name") == request_data.get("last_name")
    assert response.json().get("father_name") == request_data.get("father_name")
    assert response.json().get("date_of_enrollment") == request_data.get("date_of_enrollment")
    assert response.json().get("gender") == request_data.get("gender")


def test_create_kid_gender_failed(kids_builder):
    request_data = {
        'first_name': 'Katarina',
        'last_name': 'Kovacic',
        'father_name': 'Milan',
        'date_of_enrollment': '30-September-2020',
        'gender': 'k'
    }
    response = client.post('/kid/create_kid', json=request_data)
    assert response.status_code == 422


def test_create_kid_failed(kids_builder):
    request_data = {
        'first_name11': 'Katarina',
        'last_name': 'Kovacic',
        'father_name': 'Milan',
        'date_of_enrollment': '30-September-2020',
        'gender': 'f'
    }
    response = client.post('/kid/create_kid', json=request_data)
    assert response.status_code == 422


def test_update_kid(kids_builder):
    request_data = {
        'first_name': 'Sara',
        'last_name': 'Kovacic',
        'father_name': 'Milan',
        'date_of_enrollment': '2-Jun-2023',
        'gender': 'f'
    }

    response = client.put('/kid/1', json=request_data)
    assert response.status_code == 200


def test_update_kid_not_found(kids_builder):
    request_data = {
        'first_name': 'Sara',
        'last_name': 'Kovacic',
        'father_name': 'Milan',
        'date_of_enrollment': '2-Jun-2023',
        'gender': 'f'
    }

    response = client.put('/kid/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Kid not found.'}


def test_delete_kid(kids_builder):
    response = client.delete('/kid/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Kids).filter(Kids.id == 1).first()
    assert model is None


def test_delete_kid_not_found(kids_builder):
    response = client.delete('/kid/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Kid not found.'}
