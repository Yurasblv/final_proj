"""Domain functions for Genre"""
from src.models import db
from src.crud.abs import CRUDAbstract


def set_unknown_genre(film_id, repo: CRUDAbstract):
    """Drop genre from db"""
    return repo.remove(db_=db, id_=film_id)
