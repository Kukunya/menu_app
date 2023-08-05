from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from menu_app.crud.base import CRUDBase
from menu_app.models.submenus import Submenus


class CRUDSubmenus(CRUDBase):
	def get_items(self, db: Session, id):
		return db.query(self.model).filter(self.model.main_menu_id == id).all()

	def add(self, db: Session, data, id):
		encode_data = jsonable_encoder(data,
		                               exclude={'submenus_count', 'dishes_count'})
		item = self.model(**encode_data)
		item.main_menu_id = id
		db.add(item)
		db.commit()
		return item

	def update(self, db: Session, data, id):
		item = db.query(self.model).filter(self.model.id == id).first()
		if item:
			item.title = data.title
			item.description = data.description
			db.commit()
			return item


submenus = CRUDSubmenus(Submenus)
