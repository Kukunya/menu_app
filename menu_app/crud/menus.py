from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from menu_app.crud.base import CRUDBase
from menu_app.models.menus import Menus


class CRUDMenus(CRUDBase):
	def get_items(self, db: Session):
		return db.query(self.model).all()

	def add(self, db: Session, data):
		encode_data = jsonable_encoder(data,
		                               exclude={'submenus_count', 'dishes_count'})
		item = self.model(**encode_data)
		db.add(item)
		db.commit()
		return item


menus = CRUDMenus(Menus)
