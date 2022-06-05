from typing import Generic, Type, TypeVar, Any, List, Optional
from pydantic import BaseModel
from main.models import db
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db_: db, id_: Any) -> Optional[ModelType]:
        return db_.session.query(self.model).filter(self.model.id == id_).first()

    def get_multi(self, db_: db.session, *, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return db_.session.query(self.model).offset(skip).limit(limit).all()

    def remove(self, db_: db.session, *, id_: int) -> ModelType:
        obj = db_.session.query(self.model).get(id_)
        db_.session.delete(obj)
        db_.session.commit()
        return obj
