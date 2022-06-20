from src.models import *
from sqlalchemy import and_
from typing import List, Union
from src.crud.abs import CreateSchemaType, ModelType
from flask import abort


def get_id_by_name(username) -> int:
    """Method return a user id if name exists in db"""
    try:
        id_ = db.session.query(User).filter_by(username=username).first().id
        return id_
    except Exception:
        raise ValueError("User not found")


def search_user_db(obj_in: CreateSchemaType) -> Union[ModelType, Exception]:
    """Method return user model if it exists in db"""
    if db.session.query(User).filter_by(username=obj_in.username).count() >= 1:
        raise ValueError("User Exists")
    else:
        return obj_in


def search_director_in_db(directors: List) -> Director:
    """Method return director model if it exists in db"""
    for director in directors:
        db_obj = (
            db.session.query(Director)
            .filter(
                and_(
                    Director.director_name == director["director_name"],
                    Director.director_surname == director["director_surname"],
                )
            )
            .first()
        )
        if db_obj is not None:
            return db_obj
        else:
            db_obj = Director(
                director_name=director["director_name"],
                director_surname=director["director_surname"],
            )
            db.session.add(db_obj)
            db.session.commit()
            return db_obj


def search_genre_in_db(genres: List) -> Director:
    """Method return genre model if it exists in db"""
    for genre in genres:
        db_obj = (
            db.session.query(Genre)
            .filter(Genre.genre_name == genre["genre_name"])
            .first()
        )
        if db_obj is not None:
            db_obj.as_dict()
            return db_obj
        else:
            db_obj = Genre(genre_name=genre["genre_name"])
            db.session.add(db_obj)
            db.session.commit()
            return db_obj


def unknown_director(db_: db.session) -> Director:
    """Method returns unknown director model"""
    return (
        db_.session.query(Director)
        .filter(
            and_(
                Director.director_name == "unknown",
                Director.director_surname == "unknown",
            )
        )
        .first()
    )


def unknown_genre(db_: db.session) -> Director:
    """Method returns unknown genre model"""
    return db_.session.query(Genre).filter(Genre.genre_name == "unknown").first()


def login_required(user, app):
    if not user.is_authenticated:
        app.logger.info("Declined permission")
        raise abort(401, "Log in system please!")
