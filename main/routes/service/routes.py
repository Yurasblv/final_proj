"""Route module for film operations"""
import json
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from main.domain.domains_func.genre_domain import set_unknown_genre
from main.domain.domains_func.director_domain import set_unknown_director
from main.domain.domains_func.film_domain import (
    add_film,
    drop_db_film,
    get_list_of_films,
    edit_films_info,
    get_list_of_films_by_genre,
    get_list_of_films_by_director,
    get_list_of_films_by_date,
)

SERVICE = Blueprint("service", __name__)


@SERVICE.route("/storage/<int:page>", methods=["GET"])
def get_films(page):
    """Route for list films"""
    film_list = get_list_of_films(page)
    return json.dumps(film_list, indent=3, sort_keys=False, default=str)


@SERVICE.route("/storage/<int:page>/filter", methods=["GET", "POST"])
def get_film_by_filter(page):
    """Filter films with addition settings"""
    if "genre" in request.json.keys():
        films_query = get_list_of_films_by_genre(page, request.json["genre"])
        return json.dumps(films_query, indent=3, sort_keys=False, default=str)
    if "director" in request.json.keys():
        films_query = get_list_of_films_by_director(
            page=page, request_json=request.json["director"]
        )
        return json.dumps(films_query, indent=3, sort_keys=False, default=str)
    if "left_date" and "right_date" in request.json.keys():
        films_query = get_list_of_films_by_date(
            page,
            left_date=request.json["left_date"],
            right_date=request.json["right_date"],
        )
        return json.dumps(films_query, indent=3, sort_keys=False, default=str)
    else:
        current_app.logger.info("Bad Key")
        return jsonify({"msg": "Incorrect request"})


@login_required
@SERVICE.route("/profile", methods=["POST"])
def film_add():
    """Route for adding film"""
    if request.method == "POST":
        if not current_user.is_authenticated:
            current_app.logger.info("Declined permission")
            raise Exception("User dont log in,declined!")
        film = {
            "film_name": request.json["film_name"],
            "movie_description": request.json["movie_description"],
            "premier_date": request.json["premier_date"],
            "rate": request.json["rate"],
            "poster": request.json["poster"],
            "user_id": current_user.id,
        }
        directors = request.json["directors"]
        genres = request.json["genres"]
        film = add_film(film, directors, genres)
        return film.json()


@login_required
@SERVICE.route("/profile/films/u=<int:film_id>", methods=["PUT"])
def edit_film(film_id):
    """Route for edit film"""
    try:
        current_user.is_admin is True or current_user.is_active is True
    except Exception as e:
        current_app.logger.warning({f"{e}"})
        return "Dont have permissions"
    upd_data = request.get_json()
    edit = edit_films_info(film_id=film_id, upd_data=upd_data)
    return jsonify({"Upd": edit})


@login_required
@SERVICE.route("/profile/d=<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    """Route for removing film"""
    try:
        current_user.is_admin is True or current_user.is_active is True
    except Exception as e:
        current_app.logger.warning({f"{e}"})
        return "Dont have permissions"
    dropped_film = drop_db_film(film_id)
    return jsonify({"Dropped": dropped_film.id})


@login_required
@SERVICE.route(
    "/profile/film/<int:film_id>/director/<int:director>", methods=["PUT", "DELETE"]
)
def delete_director(film_id, director):
    """Delete director"""
    try:
        current_user.is_admin is True or current_user.is_active is True
    except Exception as e:
        current_app.logger.warning({f"{e}"})
        return "Dont have permissions"
    try:
        set_unknown_director(film_id, director)
    except Exception as e:
        current_app.logger.info({e})
        return e
    return jsonify({"msg": "Dropped"})


@login_required
@SERVICE.route(
    "/profile/film/<int:film_id>/genre/<int:genre>", methods=["PUT", "DELETE"]
)
def delete_genre(film_id, genre):
    """Delete genre"""
    try:
        current_user.is_admin is True or current_user.is_active is True
    except Exception as e:
        current_app.logger.warning({f"{e}"})
        return "Dont have permissions"
    try:
        set_unknown_genre(film_id, genre)
    except Exception as e:
        current_app.logger.info({e})
        return e
    return jsonify({"msg": "Dropped"})
