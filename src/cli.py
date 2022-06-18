import random
import faker
import string
from flask import Blueprint
from src.services.film import add_film
from src.services.user import user_create
from src.crud.user import user_repo

COMMANDS = Blueprint("commands", __name__, cli_group=None)
FAKER_INSTANCE = faker.Faker()
LETTERS = string.ascii_lowercase


def seed_users():
    for _ in range(100):
        user_create(
            repo=user_repo,
            data={
                "username": f"{FAKER_INSTANCE.user_name().capitalize()}",
                "password": f"{''.join(random.choice(LETTERS) for _ in range(10))}",
                "is_admin": False,
            },
        )
    for _ in range(10):
        user_create(
            repo=user_repo,
            data={
                "username": f"{FAKER_INSTANCE.user_name().capitalize()}",
                "password": f"{''.join(random.choice(LETTERS) for _ in range(10))}",
                "is_admin": True,
            },
        )


def seed_films():
    for _ in range(100):
        db_obj = {
            "film_name": f"{' '.join(FAKER_INSTANCE.words(3)).capitalize()}",
            "movie_description": FAKER_INSTANCE.sentence(8),
            "premier_date": FAKER_INSTANCE.date_object(),
            "rate": random.randint(1, 10),
            "poster": f"{FAKER_INSTANCE.text()}/{FAKER_INSTANCE.word()}",
            "user_id": f"{random.randint(1, 100)}",
        }
        directors = [
            {
                "director_name": f"{FAKER_INSTANCE.name().capitalize()}",
                "director_surname": f"{FAKER_INSTANCE.name().capitalize()}",
            },
            {
                "director_name": f"{FAKER_INSTANCE.name().capitalize()}",
                "director_surname": f"{FAKER_INSTANCE.name().capitalize()}",
            },
        ]
        genres = [{"genre_name": f"{FAKER_INSTANCE.word()}"}]
        add_film(directors=directors, genres=genres, film=db_obj)


@COMMANDS.cli.command("create")
def create():
    seed_users()
    seed_films()
