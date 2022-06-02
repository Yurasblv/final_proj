from typing import Optional
from pydantic import BaseModel, constr, validator, ValidationError


class UserSchema(BaseModel):
    username: constr(min_length=5, max_length=30)
    password: constr(min_length=5, max_length=30)
    is_active: Optional[bool] = None

    @validator("password")
    def validator(cls, value: str):
        if len(value) <= 4:
            raise ValueError("Password must be longer")
        if len(value) > 30:
            raise ValueError("Password must be shorter")
        return value


class UserAdminSchema(UserSchema):
    is_admin: bool = True


class UserInDB(UserSchema):
    id: Optional[int] = None

    class Config:
        orm_mode = True

