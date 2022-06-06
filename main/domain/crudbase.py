from typing import Any, Optional, Union, Dict, Generic,Type
from main.models import db
from json import JSONEncoder
from crudabstract import CRUDAbstract,\
    ModelType, \
    CreateSchemaType, \
    UpdateSchemaType, \
    ListSchemaType


class CRUDBase(CRUDAbstract, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db_: db, id_: Any) -> Optional[ModelType]:
        return db_.session.query(self.model).filter(self.model.id == id_).first()

    def get_multi(self, db_: db.session, *, skip: int = 0, limit: int = 10) -> Optional[ListSchemaType]:
        return db_.session.query(self.model).offset(skip).limit(limit).all()

    def create(self, db_: db.session, obj_in: CreateSchemaType) -> Type[ModelType]:
        obj_data = JSONEncoder().encode(obj_in)
        db_obj = self.model(**obj_data)  # type: ignore
        db_.add(db_obj)
        db_.commit()
        return db_obj
    
    def update(self, db_: db.session, *, db_obj: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = JSONEncoder().encode(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_.add(db_obj)
        db_.commit()
        db_.refresh(db_obj)
        return self.model

    def remove(self, db_: db.session, *, id_: int) -> ModelType:
        obj = db_.session.query(self.model).get(id_)
        db_.session.delete(obj)
        db_.session.commit()
        return obj

