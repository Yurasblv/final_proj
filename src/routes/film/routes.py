"""Route module for film operations"""
from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, current_app
from flask_login import login_required, current_user
from src.crud.film import film_repo
from src.crud.director import director_repo
from src.services.genre import set_unknown_genre
from src.crud.genre import genre_repo
from src.services.director import delete_director
from src.services.film import (
    add_film,
    drop_db_film,
    get_list_of_films,
    edit_films_info,
    get_list_of_films_by_genre,
    get_list_of_films_by_director,
    get_list_of_films_by_date,
    get_list_sorted_by_field,
)

apifilms = Namespace("general", description="APIs Film RESTful methods")
apimethods = Namespace(
    "personal", path="/profile", description="APIs Film RESTful methods"
)

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

filter_director = apifilms.model(
    "Filter_Director",
    {
        "director": fields.Nested(model=director_model),
    },
)
filter_genre = apifilms.model(
    "Filter_Genre",
    {
        "genre": fields.Nested(model=genre_model),
    },
)

filter_date = apifilms.model(
    "Filter_Date",
    {
        "left_date": fields.Date(default=None),
        "right_date": fields.Date(default=None),
    },
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
    },
)


@apifilms.route("/", methods=["GET"])
@apifilms.doc(params={"film_name": "Name of Film", "page": "page_num"})
class ListFilms(Resource):
    def get(self):
        """Route for list all with pagination films"""
        film_name = request.args.get("film_name").capitalize()
        page = int(request.args.get("page"))
        film_list = get_list_of_films(page, film_name, repo=film_repo)
        return jsonify(film_list)


@apifilms.route("/<int:page>/filtered=director", methods=["POST"])
class FilmFilteredDirector(Resource):
    @apifilms.expect(filter_director)
    @login_required
    def post(self, page):
        """Filter films director"""
        films_query = get_list_of_films_by_director(
            page=page, request_json=request.json["director"], repo=film_repo
        )
        return jsonify(films_query)


@apifilms.route("/<int:page>/filtered=genre", methods=["POST"])
class FilmFilteredGenre(Resource):
    @apifilms.expect(filter_genre)
    @login_required
    def post(self, page):
        """Filters films by range of genre"""
        films_query = get_list_of_films_by_genre(
            page, request.json["genre"], repo=film_repo
        )
        return jsonify(films_query)


@apifilms.route("/<int:page>/filtered=date", methods=["POST"])
class FilmFilteredDate(Resource):
    @apifilms.expect(filter_date)
    @login_required
    def post(self, page):
        """Filters films by range of dates"""
        films_query = get_list_of_films_by_date(
            page,
            left_date=request.json["left_date"],
            right_date=request.json["right_date"],
            repo=film_repo,
        )
        return jsonify(films_query)


@apifilms.route("/<int:page>/sort=rate", methods=["GET"])
class FilmSortedByRate(Resource):
    @login_required
    def post(self, page):
        """Sort films by premier date and rate"""
        sort_result = get_list_sorted_by_field(page=page, field="rate", repo=film_repo)
        return jsonify(sort_result)


@apifilms.route("/<int:page>/sort=premier_date", methods=["GET"])
class FilmSortedByPremier(Resource):
    @login_required
    def get(self, page):
        """Sort films by premier date and rate"""
        sort_result = get_list_sorted_by_field(
            page=page, field="premier_date", repo=film_repo
        )
        return jsonify(sort_result)


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
                "film_name": request.json["film_name"].capitalize(),
                "movie_description": request.json["movie_description"],
                "premier_date": request.json["premier_date"],
                "rate": request.json["rate"],
                "poster": request.json["poster"],
                "user_id": current_user.id,
            }
            directors = request.json["directors"]
            genres = request.json["genres"]
            film = add_film(
                film=film, directors=directors, genres=genres, repo=film_repo
            )
            return jsonify(film)


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
        return jsonify(edit)


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
        drop_db_film(repo=film_repo, id_=film_id)
        return jsonify({"msg": "Dropped"})


@apimethods.route("/film/<int:film_id>/del=director", methods=["DELETE"])
class DirectorDelete(Resource):
    @login_required
    def delete(self, film_id):
        """Delete director"""
        try:
            current_user.is_admin is True or current_user.is_active is True
        except Exception as e:
            current_app.logger.warning({f"{e}"})
            return "Dont have permissions"
        data = delete_director(repo=director_repo, film_id=film_id)
        return jsonify({"director": data})


@apimethods.route("/film/<int:film_id>/del=genre", methods=["DELETE"])
class GenreDelete(Resource):
    @login_required
    def delete(self, film_id):
        """Delete genre"""
        try:
            current_user.is_admin is True or current_user.is_active is True
        except Exception as e:
            current_app.logger.warning({f"{e}"})
            return "Dont have permissions"
        data = set_unknown_genre(film_id, repo=genre_repo)
        return jsonify({"genre": data})
