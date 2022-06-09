"""Module with director schema"""
from pydantic import BaseModel, constr


class DirectorBase(BaseModel):
    """Schema data"""
    director_name: constr(max_length=50)
    director_surname: constr(max_length=50)

    class Config:
        orm_mode = True
