import pytest
from run import app
from config import TestConfig
from src.models import db


@pytest.fixture(scope="function", autouse=True)
def client():
    flask_app = app
    flask_app.config.from_object(TestConfig)
    flask_app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://test:test@localhost/testdata"
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="function", autouse=True)
def app_with_db(client):
    """Fixture with empty test database"""
    db.create_all()
    yield client
    db.drop_all()
