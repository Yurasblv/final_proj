from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import ModelType, CRUDAbstract
from main.shemas.film_shema import GenreBase
from main.models import db, Genre


class GenresCRUD(CRUDBase[Genre, GenreBase, GenreBase], CRUDAbstract):
    def delete_genre(self, db_: db.session, obj_in: GenreBase) -> ModelType:
        ...


genre = GenresCRUD(Genre)
