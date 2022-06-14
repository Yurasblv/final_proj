"""Domain functions for Genre"""
from main.models import db
from main.domain.genre_repo import genre_repo
from main.domain.crudabstract import ModelType


def set_unknown_genre(film_id, genre) -> ModelType:
    """Drop genre from db"""
    ans = genre_repo.delete_genre(db_=db, film_id=film_id, genre=genre)
    return ans
