"""Test module with units for crud"""
import pytest
from src.crud.user import CRUDUser
from src.models import User, db
from src.schemas.user import UserSchema


@pytest.fixture
def user_repo():
    repo = CRUDUser(User)
    return repo


@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpassword", "is_admin": False}


@pytest.fixture
def admin_data():
    return {"username": "testadmin", "password": "testpassword", "is_admin": True}


@pytest.fixture()
def user_schema(user_data):
    schema = UserSchema(**user_data)
    return schema


@pytest.fixture()
def admin_schema(admin_data):
    schema = UserSchema(**admin_data)
    return schema


def test_user_repo_create(user_repo, user_schema):
    response = user_repo.create(db_=db, obj_in=user_schema)
    assert response.id == 1
    assert response.username == user_schema.username
    assert response.check_password(user_schema.password) is True
    assert response.is_admin is False


def test_admin_repo_create(user_repo, admin_schema):
    response = user_repo.create(db_=db, obj_in=admin_schema)
    assert response.id == 1
    assert response.username == admin_schema.username
    assert response.check_password(admin_schema.password) is True
    assert response.is_admin is True
