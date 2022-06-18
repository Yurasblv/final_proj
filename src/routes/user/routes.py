"""Route module for user and admin operations"""
from flask import request, jsonify
from src.services.user import user_create, auth_user
from flask_login import login_required, current_user, logout_user, login_user
from flask import current_app
from flask_restx import Resource, Namespace, fields
from pydantic import ValidationError
from src.crud.user import user_repo

apiregister = Namespace("registration", description="APIs Film RESTful methods")
apiuser = Namespace("authentication", description="APIs Film RESTful methods")
apilogout = Namespace("logout")

user = apiuser.model(
    "User Register",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
        "is_admin": fields.Boolean(default=False, description="Role for admin"),
    },
)


@apiregister.route("/", methods=["POST"])
@apiregister.response(500, description="User already in db")
@apiregister.response(200, description="Success")
class Registration(Resource):
    @apiregister.doc(body=user)
    @apiregister.param("payload", "**is_admin param choose: True|False", _in="body")
    def post(self):
        """Route for user or admin registration"""
        data = request.get_json()
        try:
            user = user_create(data, repo=user_repo)
        except ValidationError as e:
            return jsonify(e.errors())
        current_app.logger.info(f"{user.username} was created!")
        return jsonify({"msg": "Registered"})


@apiuser.route("/", methods=["POST"])
@apiuser.response(200, "Logged in")
@apiuser.response(500, "User not found")
class Login(Resource):
    @apiuser.doc(body=user)
    @apiuser.param("payload", _in="body")
    def post(self):
        """Route for user or admin authentication"""
        if request.method == "POST":
            data = request.json
            if current_user.is_authenticated:
                return jsonify({"msg": "already logged"})
            user = auth_user(data, repo=user_repo)
            login_user(user, remember=True)
            current_app.logger.info(f"{user.username} login")
            return jsonify({user.id: f" is_active={data['username']}"})


@apilogout.route("/", methods=["GET"])
@apilogout.response(200, description="Logged out")
class Logout(Resource):
    @login_required
    def get(self):
        """Route for user or admin log out process"""
        logout_user()
        return jsonify({"msg": "Logged out"})
