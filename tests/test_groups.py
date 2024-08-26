from starlette import status

from app.db.models import Groups
from tests.conftest import client, TestingSessionLocal
from tests.utils import groups_builder, employees_builder, kids_builder, get_access_token


def test_read_all_groups(groups_builder, get_access_token):
    response = client.get(
        "/group",
        headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_read_all_groups_not_authorized(groups_builder):
    response = client.get("/group")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_one_group(groups_builder, get_access_token):
    response = client.get(
        "/group/id/1",
        headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("name") == 'Test 0'


def test_read_one_group_not_authorized(groups_builder):
    response = client.get("/group/id/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_one_group_not_found(groups_builder, get_access_token):
    response = client.get(
        "/group/id/999",
        headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == 404
    assert response.json().get("name") is None


def test_read_one_group_not_found_not_authorized(groups_builder):
    response = client.get("/group/id/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_group(groups_builder, get_access_token):
    request_data = {'name': 'Tigrici'}
    response = client.post('/group/create_group', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 201
    assert response.json().get("name") == request_data.get("name")


def test_create_group_not_authorized(groups_builder):
    response = client.post("/group/create_group")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_group_failed(groups_builder, get_access_token):
    request_data = {'namee': 'Tigrici'}
    response = client.post('/group/create_group', json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 422


def test_create_group_failed_not_authorized(groups_builder):
    response = client.post("/group/create_group")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_group_employee(groups_builder, employees_builder, get_access_token):
    request_data = {'employee_id': 1}
    response = client.patch("/group/employee/1", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("employee") == "Test 0 User 0"


def test_update_group_employee_not_authorized(groups_builder):
    response = client.patch("/group/employee/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_group_employee_already_exist(groups_builder, employees_builder, get_access_token):
    request_data = {'employee_id': 1}
    response = client.patch("/group/employee/1", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200
    request_data = {'employee_id': 1}
    response = client.patch("/group/employee/1", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json().get('detail') == "Employee already has a group."


def test_update_group_employee_already_exist_not_authorized(groups_builder):
    response = client.patch("/group/employee/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_group_employee_group_not_found(groups_builder, employees_builder, get_access_token):
    request_data = {'employee_id': 5}
    response = client.patch("/group/employee/5", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404


def test_update_group_employee_group_not_found_not_authorized(groups_builder):
    response = client.patch("/group/employee/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_group_kid(groups_builder, kids_builder, get_access_token):
    request_data = {'kids_ids': [1, 2, 3]}
    response = client.patch("/group/kids/1", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200


def test_update_group_kid_not_authorized(groups_builder):
    response = client.patch("/group/kids/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_group_kid_already_exist(groups_builder, kids_builder, get_access_token):
    request_data = {'kids_ids': [1, 2, 3]}
    response = client.patch("/group/kids/1", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200
    request_data = {'kids_ids': [1, 2, 3]}
    response = client.patch("/group/kids/2", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json().get('detail') == 'Kid already has a group.'


def test_update_group_kid_already_exist_not_authorized(groups_builder):
    response = client.patch("/group/kids/2")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_group_kid_not_found(groups_builder, kids_builder, get_access_token):
    request_data = {'kids_ids': [1, 2, 3]}
    response = client.patch("/group/kids/10", json=request_data, headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404


def test_update_group_kid_not_found_not_authorized(groups_builder):
    response = client.patch("/group/kids/10")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_group(groups_builder, get_access_token):
    response = client.delete('/group/1', headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Groups).filter(Groups.id == 1).first()
    assert model is None


def test_delete_group_not_authorized(groups_builder):
    response = client.delete("/group/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_group_not_found(groups_builder, get_access_token):
    response = client.delete('/group/999', headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Group not found.'}


def test_delete_group_not_found_not_authorized(groups_builder):
    response = client.delete("/group/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
