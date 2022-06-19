"""Repository for User CRUD"""
from src.crud.base import CRUDBase
from src.crud.userbase import ModelType, AbstractUser
from src.schemas.user import UserSchema, UserInDB
from src.models import db, User
from typing import Dict, Any, Union
from src.use_case import search_user_db, get_id_by_name


class CRUDUser(CRUDBase[User, UserSchema, UserSchema], AbstractUser):
    """Main class for regular user"""

    def create(
        self, db_: db.session, obj_in: Union[UserSchema, Dict[str, Any]], **kwargs
    ) -> ModelType:
        """Register user"""
        valid_obj = search_user_db(obj_in)
        db.obj = self.model(**valid_obj.dict())
        db.obj.set_password(db.obj.password)
        db_.session.add(db.obj)
        db_.session.commit()
        return db.obj

    def login_user(self, db_: db.session, *, obj_in: UserInDB) -> ModelType:
        """Login user"""
        id_ = get_id_by_name(obj_in.username)
        obj = self.get(db_, id_=id_)
        if obj.check_password(obj_in.password):
            obj.is_active = True
            db_.session.add(obj)
            db_.session.commit()
            return obj
        else:
            raise ValueError("Password is not valid")


user_repo = CRUDUser(User)
