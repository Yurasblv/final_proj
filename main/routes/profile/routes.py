"""Route module for user and admin operations"""
from flask import request, jsonify
from main.domain.domains_func.register_domain import user_create, admin_create
from main.domain.domains_func.login_domain import auth_user
from flask_login import login_required, current_user, logout_user, login_user
from flask import current_app
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

apireg = Namespace("registration")

reg_user = apireg.model(
    "User Register",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
        "is_admin": fields.Boolean(default=False, description="Role for admin"),
    },
)


@apireg.route("/", methods=["POST"])
class Registration(Resource):
    @apireg.doc(body=reg_user)
    @apireg.param("payload", "**is_admin param choose: True|False", _in="body")
    def post(self):
        """Route for user or admin registration"""
        data = request.get_json()
        if data["is_admin"] is False:
            try:
                user = user_create(data)
            except ValidationError as e:
                return e.errors()
            current_app.logger.info(f"{user.username} was created!")
            return jsonify({"msg": "Registered"})
        if data["is_admin"] is True:
            try:
                admin = admin_create(data)
            except ValidationError as e:
                return e.errors()
            current_app.logger.info(f"{admin.username} admin role was created")
            return jsonify({"msg": "Registered"})


apilogin = Namespace("login")

log_user = apilogin.model(
    "User Login",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


@apilogin.route("/", methods=["POST"])
class Login(Resource):
    @apilogin.doc(body=log_user)
    @apilogin.param("payload", _in="body")
    def post(self):
        """Route for user or admin authentication"""
        if request.method == "POST":
            data = request.json
            if current_user.is_authenticated:
                return jsonify({"msg": "already logged"})
            user = auth_user(data)
            login_user(user)
            current_app.logger.info(f"{user.username} login")
            return jsonify({user.id: f" is_active={data['username']}"})


apilogout = Namespace("logout")


@apilogout.route("/", methods=["GET"])
class Logout(Resource):
    @login_required
    def get(self):
        """Route for user or admin log out process"""
        logout_user()
        return f"Logged out"
