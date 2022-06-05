from main.domain.crudbase import CRUDBase
from main.shemas.user_shema import UserSchema, UserAdminSchema, UserInDB
from main.models import db, User
from typing import Optional
from main.database import UserRequests


class CRUDUser(CRUDBase[User, UserSchema, UserSchema]):

    def register_user(self, db_: db.session, *, obj_in: UserSchema) -> Optional[User]:
        UserRequests.if_exists(obj_in.username)
        db.obj = User(username=obj_in.username,
                      password=obj_in.password,
                      is_active=obj_in.is_active)
        db_.session.add(db.obj)
        db_.session.commit()
        return db.obj

    def login_user(self, db_: db.session, *, obj_in: UserInDB):
        id_ = UserRequests.get_id_by_name(obj_in.username)
        obj = self.get(db_, id_=id_)
        obj.is_active = True
        db_.session.add(obj)
        db_.session.commit()
        return obj

    def logout_active(self, db_: db.session, *, obj_in: int):
        obj = self.get(db_, id_=obj_in)
        obj.is_active = False
        db_.session.add(obj)
        db_.session.commit()
        return obj


class CRUDAdmin(CRUDBase[User, UserAdminSchema, UserAdminSchema]):

    def register_admin(self, db_: db.session, *, obj_in: UserAdminSchema) -> Optional[User]:
        UserRequests.if_exists(obj_in.username)
        db.obj = User(username=obj_in.username,
                      password=obj_in.password,
                      is_active=obj_in.is_active,
                      is_admin=obj_in.is_admin)
        db_.session.add(db.obj)
        db_.session.commit()
        return db.obj


user_repo = CRUDUser(User)
admin_repo = CRUDAdmin(User)
