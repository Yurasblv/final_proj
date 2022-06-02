from main.models import db, User


class UserRequests:

    @staticmethod
    def if_exists(username):
        if db.session.query(User).filter_by(username=username).count() >= 1:
            raise Exception('User Exists')
        else:
            return
