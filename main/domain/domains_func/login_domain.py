from flask_login import login_user
from main.models import db
from main.domain.user_repo import user_repo
from main.shemas.user_shema import UserInDB
from typing import Optional


def auth_user(data) -> Optional[UserInDB]:
    schema = UserInDB(**data)
    obj = user_repo.login_user(db, obj_in=schema)
    login_user(obj, remember=True)
    return obj


def set_active_user(id_):
    return user_repo.logout_active(db, obj_in=id_)
