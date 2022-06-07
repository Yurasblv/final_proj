from main.domain.crudbase import CRUDBase
from main.domain.crudabstract import ModelType, CRUDAbstract
from main.shemas.film_shema import DirectorBase
from main.models import db, Director


class DirectorsCRUD(CRUDBase[Director, DirectorBase, DirectorBase], CRUDAbstract):
    def delete_director(self, db_: db.session, obj_in: DirectorBase):
        ...


director_repo = DirectorsCRUD(Director)
