from flask import Flask, redirect, url_for
from config import DevConfig
from main.models import db, User, migrate
from flask_login import LoginManager
from main.cli import commands

login_manager = LoginManager()


def register_blueprint(app):
    from main.routes.profile.routes import profile
    from main.routes.service.routes import service

    app.register_blueprint(profile)
    app.register_blueprint(service)
    app.register_blueprint(commands)


def create_app():
    app = Flask(__name__)
    if app.config["ENV"] == "development":
        app.config.from_object(DevConfig)
    login_manager.init_app(app)
    login_manager.login_view = "profile.authenticate_user"
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    register_blueprint(app)

    @login_manager.user_loader
    def load_user(id_):
        return User.query.filter_by(id=id_).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("profile.authenticate_user"))

    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}

    return app
