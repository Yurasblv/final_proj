from typing import Generic, Type, TypeVar, Union, Any, Dict, List, Optional
from flask.json import JSONEncoder
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
        return db_.query(self.model).filter(self.model.id == id_).first()

    def get_multi(self, db_: db.session, *, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return db_.query(self.model).offset(skip).limit(limit).all()

    def create(self, db_: db.session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = JSONEncoder().encode(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_.session.add(db_obj)
        db_.session.commit()
        return db_obj

    def update(self,
               db_: db.session,
               *,
               db_obj: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]
               ) -> ModelType:
        obj_data = JSONEncoder().encode(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, update_data[field])
        db_.session.add(db_obj)
        db_.session.commit()
        return db_obj

    def remove(self, db_: db.session, *, id_: int) -> ModelType:
        obj = db_.query(self.model).get(id_)
        db_.session.delete(obj)
        db_.session.commit()
        return obj
