from main.domain.user_repo import user_repo, admin_repo
from main.models import db, User
from main.shemas.user_shema import UserSchema, UserAdminSchema


def user_create(data) -> User:
    schema = UserSchema(**data)
    user = user_repo.register_user(db, obj_in=schema)
    return user


def admin_create(data) -> User:
    schema = UserAdminSchema(**data)
    admin = admin_repo.register_admin(db, obj_in=schema)
    return admin
