"""Repository For Genres"""
from src.crud.base import CRUDBase
from src.crud.abs import CRUDAbstract
from src.schemas.film import GenreBase
from src.models import db, Genre, Film
from src.use_case import unknown_genre


class GenresCRUD(CRUDBase[Genre, GenreBase, GenreBase], CRUDAbstract):
    def remove(self, db_: db.session, *, id_: int) -> str:
        """Delete genre instance"""
        film = Film.query.filter_by(id=id_).first()
        film.genres.clear()
        genre = unknown_genre(db_)
        film.genres.append(genre)
        db_.session.add(film)
        db_.session.commit()
        data = " ".join([item.genre_name for item in film.genres])
        return data


genre_repo = GenresCRUD(Genre)
