"""Schema for Film model"""
from typing import Optional, List
from pydantic import BaseModel, conint
from datetime import date
from .genre import GenreBase
from .director import DirectorBase


class FilmSchema(BaseModel):
    """Schema data"""

    film_name: str
    movie_description: str
    premier_date: date
    rate: conint(ge=0, le=10)
    poster: str
    genres: Optional[List[GenreBase]]
    directors: Optional[List[DirectorBase]]
    user_id: int

    class Config:
        orm_mode = True


class FilmListSchema(FilmSchema):
    """Schema for list Film data"""

    class Config:
        orm_mode = True
