"""Schema for User model"""
from typing import Optional
from pydantic import BaseModel, constr, validator


class UserSchema(BaseModel):
    """Schema for regular user data"""

    username: constr(min_length=4, max_length=30)
    password: constr(min_length=4, max_length=30)
    is_admin: bool

    @validator("username")
    def u_validator(cls, value: str):
        if len(value) < 4:
            raise ValueError("Username too short")
        if len(value) > 30:
            raise ValueError("Username too long")
        return value

    @validator("password")
    def p_validator(cls, value: str):
        if len(value) < 4:
            raise ValueError("Password too short")
        if len(value) > 30:
            raise ValueError("Password too long")
        return value


class UserInDB(UserSchema):
    """Schema for all users data"""

    id: Optional[int] = None

    class Config:
        orm_mode = True
