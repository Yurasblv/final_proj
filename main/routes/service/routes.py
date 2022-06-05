from flask import Blueprint

service = Blueprint("service", __name__)


@service.route("/films")
def hello_world():
    return "Films module"
