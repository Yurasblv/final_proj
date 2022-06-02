from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_admin=False, is_active=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)


film_genre = db.Table(
    "Film_Genre",
    db.Column("film_id", db.Integer, db.ForeignKey("Film.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id")),
)

film_director = db.Table(
    "Film_Director",
    db.Column("film_id", db.Integer, db.ForeignKey("Film.id")),
    db.Column("director_id", db.Integer, db.ForeignKey("Director.id")),
)


class Genre(db.Model):
    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(25))


class Director(db.Model):
    __tablename__ = "Director"

    id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(30))
    director_surname = db.Column(db.String(30))


class Film(db.Model):
    __tablename__ = "Film"

    id = db.Column(db.Integer, primary_key=True)
    film_name = db.Column(db.VARCHAR(255))
    movie_description = db.Column(db.VARCHAR(255))
    premier_date = db.Column(db.DATE())
    rate = db.Column(db.Integer())
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    genres = db.relationship(
        "Genre", secondary=film_genre, backref=db.backref("Film", lazy="dynamic")
    )
    directors = db.relationship(
        "Director", secondary=film_director, backref=db.backref("Film", lazy="dynamic")
    )

    def __init__(self, film_name, movie_description, premier_date, rate, poster, user):
        self.film_name = film_name
        self.movie_description = movie_description
        self.premier_date = premier_date
        self.rate = rate
        self.poster = poster
        self.user = user
