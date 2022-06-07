"""Route module for film operations"""
import json

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from main.domain.domains_func.film_domain import (
    add_film,
    drop_db_film,
    get_list_of_films,
    edit_films_info,
)

service = Blueprint("service", __name__)


@login_required
@service.route("/profile", methods=["POST"])
def film_add():
    """Route for adding film"""
    if not current_user.is_authenticated:
        raise "User dont log in,declined!"
    content_type = request.headers.get("Content-Type")
    if content_type and request.method == "POST":
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
@service.route("/profile/films/u=<int:film_id>", methods=["PUT"])
def edit_film(film_id):
    """Route for edit film"""
    if current_user.is_admin is True or current_user.is_active is True:
        upd_data = request.get_json()
        edit = edit_films_info(film_id=film_id, upd_data=upd_data)
        return jsonify({"Upd": edit})
    else:
        return "Exception: User must be admin or logged in"


@login_required
@service.route("/profile/d=<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    """Route for removing film"""
    if current_user.is_admin is True or current_user.is_active is True:
        dropped_film = drop_db_film(film_id)
        return jsonify({"Dropped": dropped_film.id})
    else:
        return "Exception: User must be admin or logged in"


@service.route("/storage/<int:page>", methods=["GET"])
def get_films(page):
    """Route for list films"""
    film_list = get_list_of_films(page)
    return json.dumps(film_list, indent=3, sort_keys=False, default=str)
