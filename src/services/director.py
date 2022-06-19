"""Domain functions for Director"""
from src.models import db
from src.crud.abs import CRUDAbstract


def delete_director(film_id, repo: CRUDAbstract):
    """Drop director for db"""
    return repo.remove(db_=db, id_=film_id)
