from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from menu_app.cache.crud.cache_menus import CacheMenu, menu_cache
from menu_app.crud.base import CRUDBase
from menu_app.models.menus import Menus
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.menu_obj import MenuObj


class CRUDMenus(CRUDBase):
    def get_item(self,
                 db: Session,
                 id: str) -> MenuObj | None:

        item = CacheMenu.get_item(id)
        if not item:
            item = db.query(self.model).filter(
                self.model.id == id).first()

            if item:
                item = MenuObj(id=id,
                               title=item.title,
                               description=item.description)
                menu_cache.add_item(data=item, id=item.id)

            else:
                return None
        return item

    def get_items(self, db: Session) -> list[MenuObj]:

        return [MenuObj(id=menu.id,
                        title=menu.title,
                        description=menu.description)
                for menu in db.query(self.model).all()]

    def add(self, db: Session,
            data: BaseObj) -> MenuObj:
        encode_data = jsonable_encoder(data)
        item = self.model(**encode_data)
        db.add(item)
        db.commit()

        return MenuObj(**encode_data)

    def update(self, db: Session,
               data: BaseObj,
               id: str) -> MenuObj | None:

        menu = db.query(self.model).filter(self.model.id == id).first()
        if menu:
            menu.title = data.title
            menu.description = data.description
            db.commit()
            data = data.model_dump(exclude='id')
            CacheMenu.update_item(id=id, data=data)

            return MenuObj(id=id, **data)

        return None

    def delete(self, id: str,
               db: Session) -> bool:

        if db.query(self.model).filter(self.model.id == id).delete():
            menu_cache.delete_item(id)
            db.commit()

            return True
        return False


menus = CRUDMenus(Menus)
