import pytest


@pytest.fixture
def r_data():
    return {"username": "testuser", "password": "testpassword", "is_admin": False}
