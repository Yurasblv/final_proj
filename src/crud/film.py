"""Repository For Films"""
from src.crud.base import CRUDBase
from src.crud.abs import ModelType
from src.crud.filmbase import CRUDFilmBase
from src.schemas.film import FilmSchema
from src.models import db, Film, Director, Genre
from typing import List, Dict, Union, Any
from src.use_case import (
    unknown_director,
    unknown_genre,
    search_genre_in_db,
    search_director_in_db,
)


class FilmsCRUD(CRUDBase[Film, FilmSchema, FilmSchema], CRUDFilmBase):
    """Main class for repository"""

    def create(
        self, db_: db.session, *, obj_in: Union[FilmSchema, Dict[str, Any]], **kwargs
    ) -> FilmSchema:
        """Creates film model"""
        db_obj = self.model(**obj_in)
        director_obj = search_director_in_db(directors=kwargs["directors"])
        db_obj.directors.append(director_obj)
        genre_obj = search_genre_in_db(genres=kwargs["genres"])
        db_obj.genres.append(genre_obj)
        db_.session.add(db_obj)
        db_.session.commit()
        return FilmSchema.from_orm(db_obj)

    def update(
        self,
        db_: db.session,
        *,
        db_obj: ModelType,
        obj_in: Union[FilmSchema, Dict[str, Any]]
    ) -> FilmSchema:
        """Change info in film model"""
        for field in db_obj.as_dict().keys():
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
                if "directors" not in obj_in.keys() or len(obj_in.keys()) == 0:
                    director = unknown_director(db_=db_)
                    db_obj.directors.clear()
                    db_obj.directors.append(director)
                if "genres" not in obj_in.keys() or len(obj_in.keys()) == 0:
                    genre = unknown_genre(db_=db_)
                    db_obj.genres.clear()
                    db_obj.genres.append(genre)
                db_.session.add(db_obj)
                db_.session.commit()
                return FilmSchema.from_orm(db_obj)

    def get_multi(self, db_: db.session, *, page: int = 1, per_page: int = 10) -> List:
        schema_list = super().get_multi(db_=db_, page=page)
        return [FilmSchema.from_orm(film).dict() for film in schema_list]

    def remove(self, db_: db.session, *, id_: int):
        """Delete instance from db"""
        return super().remove(db_, id_=id_)

    def list_film_by_genre(self, *, page: int, request_json: dict) -> List:
        """Return list of instances"""
        record_query = (
            self.model.query.filter(self.model.genres)
            .filter(Genre.genre_name == request_json["genre_name"])
            .paginate(page, 10, False)
            .items
        )
        return [FilmSchema.from_orm(film).dict() for film in record_query]

    def list_film_by_director(self, *, page: int, request_json: dict) -> List:
        """Return list of instances"""
        record_query = (
            self.model.query.filter(self.model.directors)
            .filter(
                Director.director_name == request_json["director_name"],
                Director.director_surname == request_json["director_surname"],
            )
            .paginate(page, 10, False)
            .items
        )
        return [FilmSchema.from_orm(film).dict() for film in record_query]

    def list_film_by_date(self, *, page, left_date, right_date) -> List:
        """Return list of instances"""
        record_query = (
            self.model.query.filter(self.model.premier_date >= left_date)
            .filter(self.model.premier_date <= right_date)
            .order_by(self.model.premier_date)
            .paginate(page, 10, False)
            .items
        )
        return [FilmSchema.from_orm(film).dict() for film in record_query]

    def list_film_by_sort(self, *, page: int, field: str) -> List:
        """Sort list of instances by field"""
        if field == "premier_date":
            record_query = (
                self.model.query.order_by(self.model.premier_date.asc())
                .paginate(page, 10, False)
                .items
            )
            return [FilmSchema.from_orm(film).dict() for film in record_query]
        if field == "rate":
            record_query = (
                self.model.query.order_by(self.model.rate.asc())
                .paginate(page, 10, False)
                .items
            )
            return [FilmSchema.from_orm(film).dict() for film in record_query]


film_repo = FilmsCRUD(Film)
