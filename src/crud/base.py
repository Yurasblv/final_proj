"""Base CRUD repository"""
from typing import Any, Optional, Union, Dict, Generic, Type, List
from src.models import db
from src.crud.abs import (
    CRUDAbstract,
    ModelType,
    CreateSchemaType,
    UpdateSchemaType,
)


class CRUDBase(CRUDAbstract, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """BASE CRUD REPO CLASS"""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db_: db.session, id_: Any) -> Optional[ModelType]:
        """Get instance"""
        return db_.session.query(self.model).filter(self.model.id == id_).first()

    def get_multi(
        self, db_: db.session, *, page: int = 1, per_page: int = 10
    ) -> List[ModelType]:
        """Get list of instances"""
        record_query = self.model.query.order_by(self.model.id).paginate(
            page, per_page, False
        )
        return record_query.items

    def create(
        self, db_: db.session, obj_in: Union[CreateSchemaType, Dict[str, Any]], **kwargs
    ) -> ModelType:
        """Create instance"""
        db_obj = self.model(**obj_data)  # type: ignore
        db_.session.add(db_obj)
        db_.session.commit()
        return db_obj

    def update(
        self,
        db_: db.session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Upd instance"""
        obj_data = db_obj.as_dict()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_.session.add(db_obj)
        db_.session.commit()
        return db_obj

    def remove(self, db_: db.session, *, id_: int) -> ModelType:
        """Delete instance"""
        db_obj = db_.session.query(self.model).get(id_)
        db_.session.delete(db_obj)
        db_.session.commit()
        return db_obj
