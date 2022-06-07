from main.domain.domains_func.register_domain import user_create, admin_create
from flask import Blueprint

commands = Blueprint("commands", __name__, cli_group=None)


def seed_users():
    user_create({"username": "defaultuser", "password": "defaultpass"})
    admin_create(({"username": "defaultadmin", "password": "defaultadminpass"}))


def seed_films():
    ...


def seed_directors():
    ...


def seed_genres():
    ...


@commands.cli.command("create")
def create():
    seed_users()
    seed_films()
    seed_directors()
    seed_genres()
