"""Film crud functions"""
from src.models import db, Film
from src.crud.abs import CRUDAbstract
from typing import List, Dict, Any
from src.crud.film import film_repo
from src.crud.filmbase import CRUDFilmBase


def add_film(
    film: Dict[str, Any], genres, directors, repo: CRUDAbstract = film_repo
) -> Dict:
    """Create film"""
    return repo.create(db, obj_in=film, genres=genres, directors=directors).dict()


def edit_films_info(
    film_id, upd_data: Dict[str, Any], repo: CRUDAbstract = film_repo
) -> Dict:
    """Update film information"""
    model = db.session.query(Film).get(film_id)
    return repo.update(db, db_obj=model, obj_in=upd_data).dict()


def drop_db_film(repo: CRUDAbstract, id_: int):
    """Delete film"""
    return repo.remove(db, id_=id_)


def get_list_of_films(page: int, repo: CRUDAbstract) -> List:
    """Get list object from Film database"""
    return repo.get_multi(db_=db, page=page, per_page=10)


def get_list_of_films_by_genre(page: int, request_json, repo: CRUDFilmBase) -> List:
    """Get list object from Film database by genre"""
    return repo.list_film_by_genre(page=page, request_json=request_json)


def get_list_of_films_by_director(page: int, request_json, repo: CRUDFilmBase) -> List:
    """Get list object from Film database by director"""
    return repo.list_film_by_director(page=page, request_json=request_json)


def get_list_of_films_by_date(
    page: int, left_date: str, right_date: str, repo: CRUDFilmBase
) -> List:
    """Get list object from Film database by date"""
    return repo.list_film_by_date(page=page, left_date=left_date, right_date=right_date)


def get_list_sorted_by_field(page: int, field: str, repo: CRUDFilmBase) -> List:
    """Get list of database object from Film db sorted by special field"""
    return repo.list_film_by_sort(page=page, field=field)
