"""Repository For Genres"""
from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import ModelType, CRUDAbstract
from main.schemas.film_schema import GenreBase
from main.models import db, Genre, Film
from typing import Optional


class GenresCRUD(CRUDBase[Genre, GenreBase, GenreBase], CRUDAbstract):
    def delete_genre(
        self, db_: db.session, *, film_id: int, genre: int
    ) -> Optional[ModelType]:
        """Delete genre instance"""
        film = Film.query.filter_by(id=film_id).first()
        for genre_obj in film.genres:
            if genre_obj.id == genre:
                db_.session.delete(genre_obj)
                db_.session.commit()
                return genre_obj
            else:
                raise ValueError("Genre is not set")


genre_repo = GenresCRUD(Genre)
