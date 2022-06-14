from flask import Flask, url_for
from config import DevConfig
from main.models import db, User, migrate
from flask_login import LoginManager
from main.cli import COMMANDS
from main.log_config import log_config
from main.routes import api

LOG_MGR = LoginManager()


def register_blueprint(app):
    app.register_blueprint(COMMANDS)


def create_app():
    app = Flask(__name__)
    if app.config["ENV"] == "development":
        app.config.from_object(DevConfig)
    LOG_MGR.init_app(app)
    LOG_MGR.login_view = "/Login"
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    api.init_app(app)
    log_config(app)
    register_blueprint(app)

    @LOG_MGR.user_loader
    def load_user(id_):
        return User.query.filter_by(id=id_).first()

    @LOG_MGR.unauthorized_handler
    def unauthorized():
        return url_for(endpoint="/Login")

    return app
