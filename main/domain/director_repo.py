from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import ModelType, CRUDAbstract
from main.schemas.film_schema import DirectorBase
from main.models import db, Director, Film
from typing import Optional


class DirectorsCRUD(CRUDBase[Director, DirectorBase, DirectorBase], CRUDAbstract):
    def delete_director(
        self, db_: db.session, *, film_id: int, director: int
    ) -> Optional[ModelType]:
        film = Film.query.filter_by(id=film_id).first()
        for director_obj in film.directors:
            if director_obj.id == director:
                db_.session.delete(director_obj)
                db_.session.commit()
                return director_obj
            else:
                raise ValueError("Director is not set")


director_repo = DirectorsCRUD(Director)
