from sqlalchemy.orm import Session
from menu_app.models.menus import Menus
from fastapi.encoders import jsonable_encoder
from menu_app.schemas.menu_obj import MenuObj


class CRUDMenus:
	def __init__(self, model):
		self.model = model

	def get_items(self, db: Session):
		menus_from_db = db.query(self.model).all()

		return [MenuObj(*i) for i in menus_from_db]

	def get_item(self, db: Session, menu_id):
		menu = db.query(self.model).filter(self.model.id == menu_id).first()

		return menu

	def add(self, db: Session, data):
		encode_data = jsonable_encoder(data, exclude={'submenus_count', 'dishes_count'})
		obj_in_data = self.model(**encode_data)
		db.add(obj_in_data)
		db.commit()

		return obj_in_data

	def update(self, db: Session, data):
		item = self.is_exist(db=db, title=data.title)
		if item:
			item.title = data.title
			item.description = data.description
			db.commit()
			return item

	def delete(self, db: Session, id):
		if db.query(self.model).filter(self.model.id == id).delete():
			db.commit()
			return True

	def is_exist(self, db: Session, title):

		return db.query(self.model).filter(self.model.title == title).scalar()


menus = CRUDMenus(Menus)
