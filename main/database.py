from main.models import db, User,Film


class UserRequests:

    @staticmethod
    def if_exists(username) -> bool:
        if db.session.query(User).filter_by(username=username).count() >= 1:
            raise Exception('User Exists')
        else:
            return False

    @staticmethod
    def get_id_by_name(username) -> int:
        try:
            id_ = db.session.query(User).filter_by(username=username).first().id
            return id_
        except Exception:
            raise "User not found"


class FilmRequests:

    @staticmethod
    def get_films(username):
        return db.session.query(Film).filter_by(username=username).all()
