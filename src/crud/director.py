from src.crud.base import CRUDBase
from src.crud.abs import CRUDAbstract
from src.schemas.film import DirectorBase
from src.models import db, Director, Film
from src.use_case import unknown_director


class DirectorsCRUD(CRUDBase[Director, DirectorBase, DirectorBase], CRUDAbstract):
    def remove(self, db_: db.session, *, id_: int) -> str:
        """Drop director instance from db"""
        film = Film.query.filter_by(id=id_).first()
        film.directors.clear()
        director = unknown_director(db_=db_)
        film.directors.append(director)
        db_.session.add(film)
        db_.session.commit()
        return " ".join([item.director_name for item in film.directors])


director_repo = DirectorsCRUD(Director)
