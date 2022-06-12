"""Route module for user and admin operations"""
from flask import Blueprint, request, jsonify
from main.domain.domains_func.register_domain import user_create, admin_create
from main.domain.domains_func.login_domain import auth_user, set_active_user
from flask_login import login_required, current_user, logout_user
from flask import current_app

PROFILE = Blueprint("profile", __name__)


@PROFILE.route("/register", methods=["POST"])
def register_user():
    """Route for user or admin registration"""
    if request.method == "POST":
        data = request.get_json()
        if "is_admin" not in data.keys():
            try:
                user = user_create(data)
                current_app.logger.info(f"{user.username} was created")
                return jsonify({"user": user.dict()})
            except ValueError as e:
                current_app.logger.info({e})
        else:
            try:
                admin = admin_create(data)
                current_app.logger.info(f"{admin.username} admin role was created")
                return jsonify({"admin_created": admin.dict()})
            except ValueError as e:
                current_app.logger.info({e})


@PROFILE.route("/user_login", methods=["POST"])
def authenticate_user():
    """Route for user or admin log in system"""
    if request.method == "POST":
        data = request.json
        if current_user.is_authenticated:
            return jsonify({"already logged": current_user.username})
        user = auth_user(data)
        current_app.logger.info(f"{user.username} user logged")
        return jsonify({user.id: f" is_active={user.is_active}"})


@login_required
@PROFILE.route("/logout", methods=["POST"])
def logout():
    """Route for user or admin log out process"""
    if request.method == "POST":
        set_active_user(current_user.id)
        logout_user()
        current_app.logger.info(f"{current_user} logged out")
        return jsonify({"user": "Logged out"})
