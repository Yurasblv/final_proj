from main.models import db
from main.domain.films_repo import film_repo
from typing import Optional, Iterable
from main.domain.crudabstract import ModelType
from main.schemas.film_schema import FilmSchema, FilmDeleteSchema, FilmListSchema


def add_film(film, directors, genres) -> Optional[ModelType]:
    film = film_repo.create_film(
        db, obj_in=FilmSchema(**film), genres=genres, directors=directors
    )
    return film


def drop_db_film(id_):
    return film_repo.delete_film(db, obj_in=FilmDeleteSchema(**{"id": id_}))


def get_list_of_films(page: int) -> Iterable:
    db_obj = film_repo.list_films(db, page=page)
    film_gen = [FilmListSchema.from_orm(film).dict() for film in db_obj]
    return film_gen


def get_list_of_films_by_genre(page: int, request_json) -> Iterable:
    db_obj = film_repo.list_film_by_genre(page=page, request_json=request_json)
    film_gen = [FilmListSchema.from_orm(film).dict() for film in db_obj]
    return film_gen


def get_list_of_films_by_director(page: int, request_json) -> Iterable:
    db_obj = film_repo.list_film_by_director(page=page, request_json=request_json)
    film_gen = [FilmListSchema.from_orm(film).dict() for film in db_obj]
    return film_gen


def get_list_of_films_by_date(page: int, left_date: str, right_date: str) -> Iterable:
    db_obj = film_repo.list_film_by_date(
        page=page, left_date=left_date, right_date=right_date
    )
    film_gen = [FilmListSchema.from_orm(film).dict() for film in db_obj]
    return film_gen


def edit_films_info(film_id, upd_data) -> ModelType:
    return film_repo.update_film(db, upd_data=upd_data, film_id=film_id)
