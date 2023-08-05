from sqlalchemy.orm import Session
from menu_app.models.dishes import Dishes
from fastapi.encoders import jsonable_encoder
from menu_app.crud.base import CRUDBase


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


dishes = CRUDDishes(Dishes)
