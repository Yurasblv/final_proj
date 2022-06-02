from flask import Flask
from config import DevConfig
from main.models import db, migrate


def register_blueprint(app):
    from main.routes.profile.routes import profile
    from main.routes.service.routes import service

    app.register_blueprint(profile)
    app.register_blueprint(service)


def create_app():
    app = Flask(__name__)
    if app.config["ENV"] == "development":
        app.config.from_object(DevConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    register_blueprint(app)
    return app
