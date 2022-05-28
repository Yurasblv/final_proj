from flask import Flask
from config import DevConfig


def register_blueprint(app):
    from main.profile.routes import profile
    from main.service.routes import service
    app.register_blueprint(profile)
    app.register_blueprint(service)


def create_app():
    app = Flask(__name__)
    if app.config["ENV"] == "dev":
        app.config.from_object(DevConfig)
    register_blueprint(app)
    return app
