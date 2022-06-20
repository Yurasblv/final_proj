"""Test module with units for crud"""
import pytest
from src.crud.film import FilmsCRUD
from src.models import User, Film, db, Genre, Director
import datetime


@pytest.fixture()
def unknown_genre():
    genre = Genre(genre_name="unknown")
    db.session.add(genre)
    db.session.commit()
    return genre


@pytest.fixture()
def unknown_director():
    director = Director(director_name="unknown", director_surname="unknown")
    db.session.add(director)
    db.session.commit()
    return director


@pytest.fixture()
def user():
    data = User(username="TEST", password="TESTPASSW", is_admin=False)
    db.session.add(data)
    db.session.commit()
    return data


@pytest.fixture
def film(user):
    film = {
        "film_name": "Strange Things",
        "movie_description": "Cool",
        "premier_date": "2022-06-20",
        "rate": 6,
        "poster": "abc.com/",
        "user_id": user.id,
    }
    return film


@pytest.fixture
def genres():
    genres = [{"genre_name": "WOW"}]
    return genres


@pytest.fixture
def directors():
    directors = [{"director_name": "Mivolas", "director_surname": "Nikolas"}]
    return directors


@pytest.fixture
def upd_data(user):
    film = {
        "film_name": "CLOWN THINGS",
        "movie_description": "Cool",
        "premier_date": "2022-06-20",
        "rate": 6,
        "poster": "abc.com/",
        "genres": [{"genre_name": "Drama"}],
        "user_id": user.id,
    }
    return film


@pytest.fixture
def film_repo():
    repo = FilmsCRUD(Film)
    return repo


def test_film_create_repo(film_repo, film, directors, genres):
    response = film_repo.create(db_=db, obj_in=film, directors=directors, genres=genres)
    assert response.film_name == film["film_name"]
    assert response.rate == film["rate"]
    assert (
        response.premier_date
        == datetime.datetime.strptime(film["premier_date"], "%Y-%m-%d").date()
    )
    assert response.poster == film["poster"]
    assert response.directors == directors
    assert response.genres == genres
    assert response.directors[0].director_name == "Mivolas"
    assert response.directors[0].director_surname == "Nikolas"
    assert response.genres[0].genre_name == "WOW"


@pytest.fixture(scope="function")
def film_db(film, directors, genres):
    model = Film(
        film["film_name"],
        film["movie_description"],
        film["premier_date"],
        film["rate"],
        film["poster"],
        film["user_id"],
    )
    director_model = Director(
        director_name=directors[0]["director_name"],
        director_surname=directors[0]["director_surname"],
    )
    genre_model = Genre(genre_name=genres[0]["genre_name"])
    model.directors.append(director_model)
    model.genres.append(genre_model)
    db.session.add(model)
    db.session.commit()
    return model


def test_film_update_repo(
    film_repo, film_db, upd_data, unknown_genre, unknown_director
):
    response = film_repo.update(db_=db, db_obj=film_db, obj_in=upd_data)
    assert response.directors[0].director_name == "unknown"
    assert response.directors[0].director_surname == "unknown"
    assert response.film_name == upd_data["film_name"]


def test_film_delete_repo(film_repo, film_db):
    response = film_repo.remove(db_=db, id_=film_db.id)
    assert response == film_db


def test_film_list_repo(film_repo, film_db):
    response = film_repo.get_multi(db_=db)
    assert len(response) == 1
