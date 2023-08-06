from uuid import UUID

from menu_app.cache.cache import r
from menu_app.cache.crud.cache_base import CacheBase
from menu_app.schemas.menu_obj import MenuObj


class CacheMenu(CacheBase):
    @staticmethod
    def get_item(id: str) -> MenuObj | None:
        obj_from_cache = r.json().get(id)
        if obj_from_cache:
            return MenuObj(**obj_from_cache)
        return None

    @staticmethod
    def add_item(id: str | UUID | None, data: MenuObj) -> None:
        r.json().set(id, '$', data.model_dump())


menu_cache = CacheMenu('')
