"""Route module for film operations"""
import json
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, current_app
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
    get_list_sorted_by_field,
)

apifilms = Namespace("films", description="APIs Film RESTful methods")


@apifilms.route("/<int:page>", methods=["GET"])
class ListFilms(Resource):
    @apifilms.param("page", "Enter page num")
    def get(self, page):
        """Route for list all with pagination films"""
        film_list = get_list_of_films(page)
        return json.dumps(film_list, indent=3, sort_keys=False, default=str)


director_model = apifilms.model(
    "Director",
    {
        "director_name": fields.String(example="Michael"),
        "director_surname": fields.String(example="Bay"),
    },
)

genre_model = apifilms.model(
    "Genre",
    {
        "genre_name": fields.String(example="Drama"),
    },
)

filters = apifilms.model(
    "Filter",
    {
        "director": fields.Nested(model=director_model),
        "genre": fields.Nested(model=genre_model),
        "left_date": fields.Date(default=None),
        "right_date": fields.Date(default=None),
    },
)


@apifilms.route("/<int:page>/filter", methods=["POST"])
class ListFilteredFilms(Resource):
    @apifilms.doc(body=filters)
    @login_required
    def post(self, page):
        """Filter films by genre,date and director"""
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


sorts = apifilms.model("Sort", {"premier_date": fields.Date(), "rate": fields.Integer})


@apifilms.route("/<int:page>/sort", methods=["POST"])
class ListSortedFilms(Resource):
    @apifilms.doc(body=sorts)
    @login_required
    def post(self, page):
        """Sort films by premier date and rate"""
        field = request.json["sort"]
        if "premier_date" or "rate" in field:
            sort_result = get_list_sorted_by_field(page=page, field=field)
            return json.dumps(sort_result, indent=3, sort_keys=False, default=str)
        else:
            current_app.logger.info("Wrong key for sort")
            return jsonify({"msg": "Wrong key"})


apimethods = Namespace(
    "profile", path="/profile", description="APIs Film RESTful methods"
)

film_create = apimethods.model(
    "Film",
    {
        "film_name": fields.String(example="Strange Things"),
        "movie_description": fields.String(example="Cool"),
        "premier_date": fields.Date,
        "rate": fields.Integer(example=6, exclusiveMax=10),
        "poster": fields.Url(example="abc.com/"),
        "genres": fields.List(fields.Nested(model=genre_model)),
        "directors": fields.List(fields.Nested(model=director_model)),
        "user_id": fields.Integer(example=1),
    },
)


@apimethods.route("/create", methods=["POST"])
class FilmCreate(Resource):
    @login_required
    @apimethods.doc(body=film_create)
    def post(self):
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
            print(dir(film))
            return jsonify(film.dict())


@apimethods.route("/film/upd=<int:film_id>", methods=["PUT"])
class FilmUpdate(Resource):
    @login_required
    @apimethods.doc(body=film_create)
    def put(self, film_id):
        """Route for edit film"""
        try:
            current_user.is_admin is True or current_user.is_active is True
        except Exception as e:
            current_app.logger.warning({f"{e}"})
            return "Dont have permissions"
        upd_data = request.get_json()
        edit = edit_films_info(film_id=film_id, upd_data=upd_data)
        return jsonify(edit.dict())


@apimethods.route("/film/del=<int:film_id>", methods=["DELETE"])
class FilmDelete(Resource):
    @login_required
    def delete(self, film_id):
        """Route for removing film"""
        try:
            current_user.is_admin is True or current_user.is_active is True
        except Exception as e:
            current_app.logger.warning({f"{e}"})
            return "Dont have permissions"
        drop_db_film(film_id)
        return jsonify({"msg": "Dropped"})


@apimethods.route("/film/<int:film_id>/director/<int:director>", methods=["DELETE"])
class DirectorDelete(Resource):
    @login_required
    def delete(self, film_id, director):
        """Delete director"""
        try:
            current_user.is_admin is True or current_user.is_active is True
        except Exception as e:
            current_app.logger.warning({f"{e}"})
            return "Dont have permissions"
        set_unknown_director(film_id, director)
        return jsonify({"msg": "Dropped"})


@apimethods.route("/film/<int:film_id>/genre/<int:genre>", methods=["DELETE"])
class GenreDelete(Resource):
    @login_required
    def delete(self, film_id, genre):
        """Delete genre"""
        try:
            current_user.is_admin is True or current_user.is_active is True
        except Exception as e:
            current_app.logger.warning({f"{e}"})
            return "Dont have permissions"
        set_unknown_genre(film_id, genre)
        return jsonify({"msg": "Dropped"})
