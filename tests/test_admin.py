from starlette import status

from app.db.models import Users
from tests.conftest import client, TestingSessionLocal
from tests.utils import get_access_token


def test_admin_read_all_authenticated(get_access_token):
    response = client.get("/admin/users", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == status.HTTP_200_OK


def test_admin_read_all_authenticated_not_authorized():
    response = client.get("/admin/users")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_delete_user(get_access_token):
    response = client.delete("/admin/users/1", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model is None


def test_admin_delete_user_not_authorized():
    response = client.delete("/admin/users/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_delete_user_not_found(get_access_token):
    response = client.delete("/admin/users/999", headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found.'}


def test_admin_delete_user_not_found_not_authorized():
    response = client.delete("/admin/users/999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
