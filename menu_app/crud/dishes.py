from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from menu_app.crud.base import CRUDBase
from menu_app.models.dishes import Dishes


class CRUDDishes(CRUDBase):
    def get_items(self, db: Session, id):
        return db.query(self.model).filter(self.model.sub_menu_id == id).all()

    def add(self, db: Session, data, id):
        encode_data = jsonable_encoder(data)
        item = self.model(**encode_data)
        item.sub_menu_id = id[0]
        item.main_menu_id = id[1]
        db.add(item)
        db.commit()
        return item

    def update(self, db: Session, data, id):
        item = db.query(self.model).filter(self.model.id == id).first()
        if item:
            item.title = data.title
            item.description = data.description
            item.price = data.price
            db.commit()
            return item


dishes = CRUDDishes(Dishes)
