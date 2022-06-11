"""Route module for user and admin operations"""
from flask import Blueprint, request, jsonify
from main.domain.domains_func.register_domain import user_create, admin_create
from main.domain.domains_func.login_domain import auth_user, set_active_user
from flask_login import login_required, current_user, logout_user
from flask import current_app

PROFILE = Blueprint("profile", __name__)


@PROFILE.route("/", methods=["POST"])
def hello_world():
    """Test route"""
    return jsonify({"msg": "Hi"})


@PROFILE.route("/register", methods=["POST"])
def register_user():
    """Route for user or admin registration"""
    content_type = request.headers.get("Content-Type")
    data = request.json
    if content_type and "is_admin" not in data.keys():
        try:
            user = user_create(data)
            current_app.logger.info(f"{user.username} was created")
            return jsonify({"user": user.dict()})
        except ValueError as e:
            current_app.logger.info({e})

    if content_type and "is_admin" in data.keys():
        try:
            admin = admin_create(data)
            current_app.logger.info(f"{admin.username} admin role was created")
            return jsonify({"admin_created": admin.dict()})
        except ValueError as e:
            current_app.logger.info({e})
    else:
        return TypeError("Set header of content-type (application/json)")


@PROFILE.route("/user_login", methods=["GET", "POST"])
def authenticate_user():
    """Route for user or admin log in system"""
    content_type = request.headers.get("Content-Type")
    data = request.json
    if current_user.is_authenticated:
        return jsonify({"already logged": current_user.username})
    if content_type:
        user = auth_user(data)
        current_app.logger.info(f"{user.username} user logged")
        return jsonify({user.id: f" is_active={user.is_active}"})


@login_required
@PROFILE.route("/logout", methods=["GET", "POST"])
def logout():
    """Route for user or admin log out process"""
    content_type = request.headers.get("Content-Type")
    if request.method == "POST" and content_type:
        set_active_user(current_user.id)
        logout_user()
        current_app.logger.info(f"{current_user} logged out")
        return jsonify({"user": "Logged out"})
