from datetime import timedelta
from fastapi import HTTPException
from jose import jwt
from app.routers.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from tests.conftest import TestingSessionLocal
from tests.utils import get_access_token
import pytest


def test_authenticate_user(get_access_token):
    db = TestingSessionLocal()
    username = 'testuser'

    authenticated_user = authenticate_user(username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == username


def test_authenticate_no_user():
    db = TestingSessionLocal()
    username = 'testuser'

    authenticated_user = authenticate_user(username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'
