"""Repository For Films"""
from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import CRUDAbstract, ModelType
from main.shemas.film_shema import FilmSchema, FilmDeleteSchema
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
                    director_name=director["name"], director_surname=director["surname"]
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
    ) -> ModelType:
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
                return self.get(db_, id_=film_id).as_dict()
        except ValueError:
            print("<< Film not found >>")

    def delete_film(self, db_: db.session, *, obj_in: FilmDeleteSchema):
        """Delete instance from db"""
        try:
            super().remove(db_, id_=obj_in.id)
            return obj_in
        except Exception:
            raise ValueError(f"\n<< Film not in database >>")

    def list_films(self, db_: db.session, *, page: int) -> List[FilmSchema]:
        """Return list of instances"""
        schema_list = super().get_multi(db_=db_, page=page)
        return schema_list


film_repo = FilmsCRUD(Film)
