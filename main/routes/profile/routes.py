from flask import Blueprint, request, jsonify, redirect, url_for
from main.domain.domains_func.register_domain import user_create, admin_create
from main.domain.domains_func.login_domain import auth_user, set_active_user
from flask_login import login_required, current_user, logout_user


profile = Blueprint("profile", __name__)


@profile.route("/", methods=["POST"])
def hello_world():
    return jsonify({"msg": "Hi"})


@profile.route("/register", methods=["POST"])
def register_user():
    content_type = request.headers.get("Content-Type")
    data = request.json
    if content_type and "is_admin" not in data.keys():
        try:
            user = user_create(data)
            return jsonify({"user": user.dict()})
        except ValueError as e:
            raise e  # logger here
    if content_type and "is_admin" in data.keys():
        try:
            admin = admin_create(data)
            return jsonify({"admin_created": admin.dict()})
        except ValueError as e:
            raise e  # logger here
    else:
        return TypeError("Set header of content-type (application/json)")


@profile.route("/user_login", methods=["GET", "POST"])
def authenticate_user():
    content_type = request.headers.get("Content-Type")
    data = request.json
    if current_user.is_authenticated:
        return jsonify({'already logged': current_user.username})
    if content_type:
        user = auth_user(data)
        return jsonify({user.id: f" is_active={user.is_active}"})


@login_required
@profile.route("/logout", methods=["GET", "POST"])
def logout():
    content_type = request.headers.get("Content-Type")
    if request.method == "POST" and content_type:
        set_active_user(current_user.id)
        logout_user()
        return jsonify({"user": "Logged out"})
