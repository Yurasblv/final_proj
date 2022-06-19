"""ABS class for USER repository """
from abc import ABC, abstractmethod
from src.models import db
from typing import TypeVar, Generic, List
from pydantic import BaseModel
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Declarative class for DB model"""

    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDFilmBase(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """ABS FILM CRUD"""

    @abstractmethod
    def list_film_by_genre(self, *, page: int, request_json: dict) -> List[BaseModel]:
        ...

    @abstractmethod
    def list_film_by_director(
        self, *, page: int, request_json: dict
    ) -> List[BaseModel]:
        ...

    @abstractmethod
    def list_film_by_date(self, *, page, left_date, right_date) -> List[BaseModel]:
        ...

    @abstractmethod
    def list_film_by_sort(self, *, page: int, field: str) -> List[BaseModel]:
        ...
