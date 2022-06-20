"""Module with config classes for development"""
from os import path, getenv
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Base config class."""

    SQLALCHEMY_DATABASE_URI = str
    SECRET_KEY = str
    SQLALCHEMY_TRACK_MODIFICATIONS = bool


class DevConfig(Config):
    """Development config."""

    load_dotenv(path.join(basedir, ".env"), override=True)
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    """Test config."""

    load_dotenv(path.join(basedir, ".env.test"), override=True)
    TESTING = getenv("TESTING")
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
