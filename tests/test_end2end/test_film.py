"""Test module for films"""
import pytest
from urllib.parse import urlencode


@pytest.fixture()
def user_data():
    return dict(username="Username", password="UPASS1", is_admin=False)


@pytest.fixture()
def film_instance():
    film = {
        "film_name": "Test ",
        "movie_description": "Test",
        "premier_date": "2000-06-19",
        "rate": 1,
        "poster": "abc.com/",
        "genres": [{"genre_name": "Senion"}],
        "directors": [{"director_name": "ORUEL", "director_surname": "Hockins"}],
    }
    return film


@pytest.fixture()
def upd_film_instance():
    upd_info = {
        "film_name": "Test ",
        "movie_description": "Test",
        "premier_date": "1992-10-02",
        "rate": 10,
        "poster": "test_poster.com/",
    }
    return upd_info


def test_create_no_auth(film_instance, app_with_db):
    response = app_with_db.post("profile/create", json=film_instance)
    assert response.status_code == 401


def test_create_with_auth(film_instance, app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    response = app_with_db.post("profile/create", json=film_instance)
    assert response.status_code == 200


def test_update_no_auth(film_instance, app_with_db, user_data):
    response = app_with_db.put("/profile/film/upd={}".format(1), json=film_instance)
    assert response.status_code == 401


def test_update_with_auth(film_instance, app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    app_with_db.post("profile/create", json=film_instance)
    response = app_with_db.put("/profile/film/upd=1", json=film_instance)
    assert response.status_code == 200


def test_get_all_films(app_with_db, user_data, film_instance):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    app_with_db.post("profile/create", json=film_instance)
    params = {"page": 1, "film_name": "te"}
    response = app_with_db.get("/general/?" + urlencode(params))
    assert response.status_code == 200
    assert type(response.data) == bytes


def test_sort_film_date_no_auth(app_with_db, user_data):
    response = app_with_db.get("/general/1/sort=premier_date")
    assert response.status_code == 401


def test_sort_film_date(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    response = app_with_db.get("/general/1/sort=premier_date")
    assert response.status_code == 200
    assert type(response.data) == bytes


def test_sort_film_rate_no_auth(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    response = app_with_db.get("/general/1/sort=rate")
    assert response.status_code == 401


def test_sort_film_rate(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    response = app_with_db.get("/general/1/sort=rate")
    assert response.status_code == 200
    assert type(response.data) == bytes


def test_filter_film_director_no_auth(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    response = app_with_db.post(
        "general/1/filtered=director",
        json={"director": {"director_name": "Michael", "director_surname": "Bay"}},
    )
    assert response.status_code == 401


def test_sort_film_director(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    response = app_with_db.post(
        "/general/1/filtered=director",
        json={"director": {"director_name": "Michael", "director_surname": "Bay"}},
    )
    assert response.status_code == 200
    assert type(response.data) == bytes


def test_filter_film_genre_no_auth(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    response = app_with_db.post(
        "general/1/filtered=genre", json={"genre": {"genre_name": "Drama"}}
    )
    assert response.status_code == 401


def test_sort_film_genre(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    response = app_with_db.post(
        "/general/1/filtered=genre", json={"genre": {"genre_name": "Drama"}}
    )
    assert response.status_code == 200
    assert type(response.data) == bytes


def test_filter_film_date_no_auth(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    response = app_with_db.post(
        "general/1/filtered=genre", json={"genre": {"genre_name": "Drama"}}
    )
    assert response.status_code == 401


def test_filter_film_date(app_with_db, user_data):
    app_with_db.post("/registration/", json=user_data)
    app_with_db.post("/authentication/", json=user_data)
    response = app_with_db.post(
        "/general/1/filtered=date",
        json={"left_date": "2022-06-20", "right_date": "2022-06-20"},
    )
    assert response.status_code == 200
    assert type(response.data) == bytes
