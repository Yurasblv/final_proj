from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    film_id = db.Column(db.Integer, db.ForeignKey('Film.id'))
    films = db.relationship("Film", db.backref("User"))

    def __init__(self, username, password, is_admin=False, is_active=False):
        self.name = username
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Film(db.Model):
    __tablename__ = 'Film'

    id = db.Column(db.Integer, primary_key=True)
    film_name = db.Column(db.VARCHAR(255))
    movie_description = db.Column(db.VARCHAR(255))
    premier_date = db.Column(db.DATE())
    rate = db.Column(db.Integer())
    poster = db.Column(db.Text)
    film_genre_id = db.Column(db.Integer, db.ForeignKey("Film_Genre.film_id"))
    genres = db.relationship("Genre", db.backref("Film"))
    film_director_id = db.Column(db.Integer, db.ForeignKey("Film_Director.film_id"))
    directors = db.relationship("Director", db.backref("Film"))

    def __init__(self, film_name, movie_description, premier_date, rate, poster):
        self.film_name = film_name
        self.movie_description = movie_description
        self.premier_date = premier_date
        self.rate = rate
        self.poster = poster



film_genre = db.Table(
    "Film_Genre",
    db.Column("film_id", db.ForeignKey("Film.id")),
    db.Column("genre_id", db.ForeignKey("Genre.id")),
)


class Genre(db.Model):
    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(25))


film_director = db.Table(
    "Film_Director",
    db.Column("film_id", db.ForeignKey("Film.id")),
    db.Column("director_id", db.ForeignKey("Director.id")),
)


class Director(db.Model):
    __tablename__ = 'Director'

    id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(30))
    director_surname = db.Column(db.String(30))
