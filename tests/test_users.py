from starlette import status
from tests.utils import get_access_token
from tests.conftest import client


def test_return_user(get_access_token):
    response = client.get("/user", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == 'testuser@example.com'
    assert response.json()['first_name'] == 'Test'
    assert response.json()['last_name'] == 'User'
    assert response.json()['role'] == 'admin'


def test_return_user_not_authorized(get_access_token):
    response = client.get("/user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password_success(get_access_token):
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "newpassword"},
                          headers={"Authorization": f"Bearer {get_access_token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_success_not_authorized(get_access_token):
    response = client.put("/user/password")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password_invalid_current_password(get_access_token):
    response = client.put("/user/password", json={"password": "wrong_password", "new_password": "newpassword"},
                          headers={"Authorization": f"Bearer {get_access_token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change.'}


def test_change_password_invalid_current_password_not_authorized(get_access_token):
    response = client.put("/user/password")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
