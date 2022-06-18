"""Domain functions for User Registration"""
from src.crud.abs import CRUDAbstract
from src.schemas.user import UserSchema
from src.models import db
from src.schemas.user import UserInDB
from src.crud.userbase import AbstractUser


def user_create(data, repo: CRUDAbstract) -> UserSchema:
    """Create Regular User Instance"""
    user_schema = UserSchema(**data)
    return repo.create(db, obj_in=user_schema)


def auth_user(data, repo: AbstractUser) -> UserInDB:
    """Login crud func"""
    schema = UserInDB(**data)
    return repo.login_user(db, obj_in=schema)
