from flask import Blueprint

profile = Blueprint("profile", __name__)

@profile.route('/profile')
def hello_world():
    return "Authorization module"
