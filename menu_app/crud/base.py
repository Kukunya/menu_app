from sqlalchemy.orm import Session

from menu_app.models.dishes import Dishes
from menu_app.models.menus import Menus
from menu_app.models.submenus import Submenus


class CRUDBase:
    def __init__(self, model):
        self.model = model

    def is_item_exist(self, db: Session,
                      title: str) -> Menus | Submenus | Dishes | None:
        return db.query(self.model).filter(self.model.title == title).first()
