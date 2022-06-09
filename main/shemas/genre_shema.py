"""Schema for Genre model"""
from pydantic import BaseModel, constr


class GenreBase(BaseModel):
    """Schema data"""
    genre_name: constr(max_length=50)

    class Config:
        orm_mode = True
