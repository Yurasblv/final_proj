"""Schema for Film model"""
from typing import Optional, List
from pydantic import BaseModel, conint
from datetime import date
from .genre_shema import GenreBase
from .director_shema import DirectorBase


class FilmSchema(BaseModel):
    """Schema data"""
    film_name: Optional[str]
    movie_description: Optional[str]
    premier_date: Optional[date]
    rate: conint(ge=0, le=10)
    poster: Optional[str]
    genres: Optional[List[GenreBase]]
    directors: Optional[List[DirectorBase]]
    user_id: int

    class Config:
        orm_mode = True


class FilmListSchema(FilmSchema):
    """Schema for list Film data"""
    class Config:
        orm_mode = True


class FilmDeleteSchema(BaseModel):
    """Schema for delete Film data"""
    id: int


# input = {
#     "film_name": "top-gun",
#     "movie_description": "New chapter of legendary series with Tom Cruise in cast",
#     "premier_date": "2022-05-10",
#     "rate": 10,
#     "poster": "poster.jpeg",
#     "genres": [
#         {
#             "genre_name": "action"
#         },
#     ],
#     "directors": [
#         {
#             "director_name": "robby",
#             "director_surname": "robbinson"
#         },
#     ],
#     "user_id": 1
# }
#
# s = FilmSchema(**input)
# print(s)
