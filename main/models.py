"""Models module with db instances"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model, UserMixin):
    """Model of User"""

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def get_id(self):
        """Return user_id"""
        return self.id

    def is_active(self):
        return True

    def set_password(self, password):
        """Set hash for password"""
        self.password = generate_password_hash(password, method="sha256", salt_length=5)

    def check_password(self, password):
        """Check hash for password"""
        return check_password_hash(self.password, password)

    def as_dict(self):
        """Return dict of model instance"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


film_genre = db.Table(
    "Film_Genre",
    db.Column(
        "film_id",
        db.Integer,
        db.ForeignKey("Film.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
    db.Column(
        "genre_id",
        db.Integer,
        db.ForeignKey("Genre.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
)

film_director = db.Table(
    "Film_Director",
    db.Column(
        "film_id",
        db.Integer,
        db.ForeignKey("Film.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
    db.Column(
        "director_id",
        db.Integer,
        db.ForeignKey("Director.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
)


class Genre(db.Model):
    """Model of Genre"""

    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(25))

    def as_dict(self):
        """Return dict of model instance"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Director(db.Model):
    """Model of Director"""

    __tablename__ = "Director"

    id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(30))
    director_surname = db.Column(db.String(30))

    def as_dict(self):
        """Return dict of model instance"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Film(db.Model):
    """Model of Film"""

    __tablename__ = "Film"

    id = db.Column(db.Integer, primary_key=True)
    film_name = db.Column(db.VARCHAR(255))
    movie_description = db.Column(db.VARCHAR(255))
    premier_date = db.Column(db.DATE())
    rate = db.Column(db.Integer())
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    genres = db.relationship(
        "Genre",
        secondary=film_genre,
        backref=db.backref("Film", lazy="dynamic"),
    )
    directors = db.relationship(
        "Director",
        secondary=film_director,
        backref=db.backref("Film", lazy="dynamic"),
    )

    def __init__(
        self, film_name, movie_description, premier_date, rate, poster, user_id
    ):
        self.film_name = film_name
        self.movie_description = movie_description
        self.premier_date = premier_date
        self.rate = rate
        self.poster = poster
        self.user_id = user_id

    def as_dict(self):
        """Return dict of model instance"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
