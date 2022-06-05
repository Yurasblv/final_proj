from flask import Blueprint, request, jsonify, redirect, url_for

service = Blueprint("service", __name__)

@service.route("/profile")
def hello_world():
    return "Films module"
