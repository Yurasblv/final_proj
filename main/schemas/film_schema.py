"""Schema for Film model"""
from typing import Optional, List
from pydantic import BaseModel, conint
from datetime import date
from .genre_schema import GenreBase
from .director_schema import DirectorBase


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


class FilmDeleteSchema(BaseModel):
    """Schema for delete Film data"""

    id: int


# from faker import Faker as f
# faker = f()
# input = {
#     "film_name": "top-gun",
#     "movie_description": "New chapter of legendary series with Tom Cruise in cast",
#     "premier_date": faker.date_object(),
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
# print(type(s.premier_date))
