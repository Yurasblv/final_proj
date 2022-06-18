"""ABS class for USER repository """
from abc import ABC, abstractmethod
from src.models import db
from typing import TypeVar, Generic
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


class AbstractUser(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    @abstractmethod
    def login_user(self, db_: db.session, *, obj_in: BaseModel):
        """Login user"""
