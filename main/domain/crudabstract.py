"""Abstract class for CRUD repository """
from abc import ABC, abstractmethod
from main.models import db
from typing import Any, Dict, List, Optional, TypeVar, Union, Generic
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


class CRUDAbstract(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """ABC CLASS"""

    @abstractmethod
    def get(self, db_: db.session, id_: Any) -> Optional[ModelType]:
        ...

    @abstractmethod
    def get_multi(
        self, db_: db.session, *, page: int, per_page: int
    ) -> List[ModelType]:
        ...

    @abstractmethod
    def create(self, db_: db.session, obj_in: CreateSchemaType) -> ModelType:
        ...

    @abstractmethod
    def update(
        self,
        db_: db.session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        ...

    @abstractmethod
    def remove(self, db_: db.session, *, id_: int) -> ModelType:
        ...
