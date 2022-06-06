from typing import Optional
from pydantic import BaseModel, conint
from datetime import date


class FilmSchema(BaseModel):
    film_name = str
    movie_description = str
    premier_date = date
    rate = conint(ge=0, le=10)
    poster = Optional[str]
