"""Domain functions for User Authorisation"""
from main.models import db
from main.domain.user_repo import user_repo
from main.schemas.user_schema import UserInDB
from typing import Optional


def auth_user(data) -> Optional[UserInDB]:
    """Login domain func"""
    schema = UserInDB(**data)
    obj = user_repo.login_user(db, obj_in=schema)
    return obj
