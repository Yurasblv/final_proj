"""Repository For Films"""
from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import CRUDAbstract
from main.schemas.film_schema import FilmSchema, FilmDeleteSchema
from main.models import db, Film, Director, Genre
from typing import List, Dict, Union, Any


class FilmsCRUD(CRUDBase[Film, FilmSchema, FilmSchema], CRUDAbstract):
    """Main class for repository"""

    def create_film(
        self, db_: db.session, *, obj_in: FilmSchema, genres, directors
    ) -> FilmSchema:
        """Creates film model"""

        db_obj = self.model(
            user_id=obj_in.user_id,
            film_name=obj_in.film_name,
            movie_description=obj_in.movie_description,
            rate=obj_in.rate,
            premier_date=obj_in.premier_date,
            poster=obj_in.poster,
        )
        for director in directors:
            db_obj.directors.append(
                Director(
                    director_name=director["director_name"],
                    director_surname=director["director_surname"],
                )
            )
        for genre in genres:
            db_obj.genres.append(Genre(genre_name=genre["genre_name"]))
        db_.session.add(db_obj)
        db_.session.commit()
        return FilmSchema.from_orm(obj_in)

    def update_film(
        self,
        db_: db.session,
        *,
        upd_data: Union[FilmSchema, Dict[str, Any]],
        film_id: int,
    ) -> FilmSchema:
        """Change info in film model"""
        try:
            db_obj = self.get(db_, id_=film_id)
            if db_obj is None:
                raise ValueError
            else:
                if isinstance(upd_data, dict):
                    update_data = upd_data
                else:
                    update_data = upd_data.dict(exclude_unset=True)
                super().update(db_, db_obj=db_obj, obj_in=update_data)
                return FilmSchema.from_orm(self.get(db_, id_=film_id))
        except ValueError:
            print("<< Film not found >>")

    def delete_film(self, db_: db.session, *, obj_in: FilmDeleteSchema):
        """Delete instance from db"""
        try:
            super().remove(db_, id_=obj_in.id)
            return obj_in
        except ValueError:
            return None

    def list_films(self, db_: db.session, *, page: int) -> List[FilmSchema]:
        """Return list of instances"""
        schema_list = super().get_multi(db_=db_, page=page)
        return schema_list

    def list_film_by_genre(self, *, page: int, request_json: dict) -> List[FilmSchema]:
        """Return list of instances"""
        record_query = (
            self.model.query.filter(self.model.genres)
            .filter(Genre.genre_name == request_json["genre_name"])
            .paginate(page, 10, False)
            .items
        )
        return record_query

    def list_film_by_director(
        self, *, page: int, request_json: dict
    ) -> List[FilmSchema]:
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
        return record_query

    def list_film_by_date(
        self, *, page, left_date, right_date
    ) -> List[FilmSchema]:  # type :ignore
        """Return list of instances"""
        record_query = (
            self.model.query.filter(self.model.premier_date >= left_date)
            .filter(self.model.premier_date <= right_date)
            .order_by(self.model.premier_date)
            .paginate(page, 10, False)
            .items
        )
        return record_query

    def list_film_by_sort(self, *, page: int, field: str):
        """Sort list of instances by field"""
        if field == "premier_date":
            record_query = (
                self.model.query.order_by(self.model.premier_date.asc())
                .paginate(page, 10, False)
                .items
            )
            return record_query
        if field == "rate":
            record_query = (
                self.model.query.order_by(self.model.rate.asc())
                .paginate(page, 10, False)
                .items
            )
            return record_query


film_repo = FilmsCRUD(Film)
