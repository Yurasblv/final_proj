"""Schema for User model"""
from typing import Optional
from pydantic import BaseModel, constr, validator


class UserSchema(BaseModel):
    """Schema for regular user data"""

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
    """Schema for admin data"""
    is_admin: bool = True


class UserInDB(UserSchema):
    """Schema for all users data"""
    id: Optional[int] = None

    class Config:
        orm_mode = True
