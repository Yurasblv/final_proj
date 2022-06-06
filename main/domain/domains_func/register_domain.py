from main.domain.user_repo import user_repo, admin_repo
from main.models import db
from main.shemas.user_shema import UserSchema, UserAdminSchema
from typing import Optional


def user_create(data) -> Optional[UserSchema]:
    schema = UserSchema(**data)
    user_repo.register_user(db, obj_in=schema)
    return schema


def admin_create(data) -> Optional[UserAdminSchema]:
    schema = UserAdminSchema(**data)
    admin_repo.register_admin(db, obj_in=schema)
    return schema
