"""Domain functions for Director"""
from main.models import db
from main.domain.director_repo import director_repo
from main.domain.crudabstract import ModelType


def set_unknown_director(film_id, directors) -> ModelType:
    """Drop director for db"""
    ans = director_repo.delete_director(db_=db, film_id=film_id, director=directors)
    return ans
