from flask import Blueprint, request, jsonify
from main.domain.domains_func.user_create import user_create,admin_create

profile = Blueprint("profile", __name__)


@profile.route("/", methods=['POST'])
def hello_world():
    return jsonify({'msg': 'Hi'})


@profile.route("/register", methods=['POST'])
def register_user():
    content_type = request.headers.get('Content-Type')
    data = request.json
    if content_type and 'is_admin' not in data.keys():
        try:
            user = user_create(data)
            return jsonify({'registered': user.username})
        except Exception:
            raise ValueError  # logger here
    if content_type and 'is_admin' in data.keys():
        try:
            admin = admin_create(data)
            return jsonify({'admin_created': admin.username})
        except Exception:
            raise ValueError
    else:
        raise TypeError("Set header of content-type (application/json)")


@profile.route("/login", methods=['GET', 'POST'])
def authenticate_user():
    ...
