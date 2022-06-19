import pytest


@pytest.fixture()
def user_data():
    return dict(username="Username", password="UPASS1", is_admin=False)


def test_register_user(app_with_db, user_data):
    response1 = app_with_db.post("/registration/", json=user_data)
    assert response1.status_code == 200
    assert response1.json == {"msg": "Registered"}
    with pytest.raises(Exception):
        app_with_db.post("/registration/", json=user_data)


@pytest.fixture()
def admin_data():
    return dict(username="ADMIN123456", password="ADMPASS1", is_admin=True)


def test_register_admin(app_with_db, admin_data):
    response1 = app_with_db.post("/registration/", json=admin_data)
    assert response1.status_code == 200
    assert response1.json == {"msg": "Registered"}
    with pytest.raises(Exception):
        app_with_db.post("/registration/", json=admin_data)


@pytest.fixture()
def incorrect_user_data_1():
    return dict(username="U1", password="2", is_admin=False)


@pytest.fixture()
def incorrect_user_data_2():
    return dict(username="USernAme1345", password="11", is_admin=False)


@pytest.fixture()
def incorrect_user_data_3():
    return dict(username="U", password="1143w6345ghg", is_admin=True)


def test_incorrect_user(
    app_with_db, incorrect_user_data_1, incorrect_user_data_2, incorrect_user_data_3
):
    response1 = app_with_db.post("/registration/", json=incorrect_user_data_1)
    assert response1.status_code == 200
    assert response1.json == [
        {
            "ctx": {"limit_value": 4},
            "loc": ["username"],
            "msg": "ensure this value has at least 4 characters",
            "type": "value_error.any_str.min_length",
        },
        {
            "ctx": {"limit_value": 4},
            "loc": ["password"],
            "msg": "ensure this value has at least 4 characters",
            "type": "value_error.any_str.min_length",
        },
    ]
    response2 = app_with_db.post("/registration/", json=incorrect_user_data_2)
    assert response2.status_code == 200
    assert response2.json == [
        {
            "ctx": {"limit_value": 4},
            "loc": ["password"],
            "msg": "ensure this value has at least 4 characters",
            "type": "value_error.any_str.min_length",
        }
    ]
    response3 = app_with_db.post("/registration/", json=incorrect_user_data_3)
    assert response3.status_code == 200
    assert response3.json == [
        {
            "ctx": {"limit_value": 4},
            "loc": ["username"],
            "msg": "ensure this value has at least 4 characters",
            "type": "value_error.any_str.min_length",
        }
    ]


def test_login_admin_role(app_with_db, admin_data):
    response = app_with_db.post("/login/", json=admin_data)
    assert response.status_code == 200
    repeat_data = admin_data
    response2 = app_with_db.post("/login/", json=repeat_data)
    assert response2.json == {"msg": "already logged"}
