from main.domain.crudbase import CRUDBase
from main.shemas.film_shema import FilmSchema
from main.models import db, Film, User
from typing import Optional


class FilmsCRUD(CRUDBase[Film, FilmSchema, FilmSchema]):

    def create_film(self, db_: db.session, *, obj_in: FilmSchema):
        ...

