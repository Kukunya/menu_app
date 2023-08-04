from sqlalchemy.orm import Session
from menu_app.models.menus import Menus
from menu_app.models.dishes import Dishes
from menu_app.models.submenus import Submenus
from sqlalchemy import distinct, func


class CRUDMenus:
	def __init__(self, model):
		self.model = model

	def get_items(self, db: Session):
		menus_id, menus = db.query(self.model.id, self.model).all()

		return [menu for menu in db.query(self.model).all()]

	def get_item(self, db: Session, id):
		return db.query(self.model).filter(self.model.id == id).first()

	def add(self, db: Session, data):

		obj_in_data = self.model(**data)
		db.add(obj_in_data)
		db.commit()
		return obj_in_data

	def is_exist(self, db: Session, title):
		return db.query(self.model).filter(self.model.title == title).scalar()


menus = CRUDMenus(Menus)
a = (1, 2, 3,)
a += (4,)
print(a)