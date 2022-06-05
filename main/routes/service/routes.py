from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_required

service = Blueprint("service", __name__)


@login_required
@service.route("/profile")
def hello_world():
    return "Films module"
