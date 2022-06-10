"""Repository for User CRUD"""
from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import ModelType, CRUDAbstract
from main.shemas.user_shema import UserSchema, UserAdminSchema, UserInDB
from main.models import db, User
from typing import Optional


class CRUDUser(CRUDBase[User, UserSchema, UserSchema], CRUDAbstract):
    """Main class for regular user"""

    @staticmethod
    def get_id_by_name(username) -> int:
        """Method return a user id if name exists in db"""
        try:
            id_ = db.session.query(User).filter_by(username=username).first().id
            return id_
        except Exception:
            raise "User not found"

    def register_user(
        self, db_: db.session, *, obj_in: UserSchema
    ) -> Optional[ModelType]:
        """Register user"""
        if (
            db.session.query(self.model).filter_by(username=obj_in.username).count()
            >= 1
        ):
            raise Exception("User Exists")
        else:
            db.obj = self.model(
                username=obj_in.username,
                password=obj_in.password,
                is_active=obj_in.is_active,
            )
            db.obj.set_password(db.obj.password)
            db_.session.add(db.obj)
            db_.session.commit()
            return db.obj

    def login_user(self, db_: db.session, *, obj_in: UserInDB):
        """Login user"""
        id_ = CRUDUser.get_id_by_name(obj_in.username)
        obj = self.get(db_, id_=id_)
        try:
            obj.check_password(obj_in.password)
        except ValueError:
            raise "Password not valid"
        obj.is_active = True
        db_.session.add(obj)
        db_.session.commit()
        return obj

    def logout_active(self, db_: db.session, *, obj_in: int):
        """Log out user with changing status"""
        obj = self.get(db_, id_=obj_in)
        obj.is_active = False
        db_.session.add(obj)
        db_.session.commit()
        return obj


class CRUDAdmin(CRUDBase[User, UserAdminSchema, UserAdminSchema], CRUDAbstract):
    """Main class for Admin role"""

    def register_admin(
        self, db_: db.session, *, obj_in: UserAdminSchema
    ) -> Optional[User]:
        """Creates admin instance in db"""
        if (
            db.session.query(self.model).filter_by(username=obj_in.username).count()
            >= 1
        ):
            raise Exception("User Exists")
        else:
            db.obj = self.model(
                username=obj_in.username,
                password=obj_in.password,
                is_active=obj_in.is_active,
                is_admin=obj_in.is_admin,
            )
            db.obj.set_password(db.obj.password)
            db_.session.add(db.obj)
            db_.session.commit()
            return db.obj


user_repo = CRUDUser(User)
admin_repo = CRUDAdmin(User)
