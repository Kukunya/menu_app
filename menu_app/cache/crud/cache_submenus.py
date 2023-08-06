from redis.commands.json.path import Path

from menu_app.cache.cache import r
from menu_app.cache.crud.cache_base import CacheBase
from menu_app.schemas.submenu_obj import SubmenuObj


class CacheSubmenu(CacheBase):
    @staticmethod
    def get_item(id: str) -> SubmenuObj | None:
        obj_from_cache = r.json().get(id)
        if obj_from_cache:
            return SubmenuObj(**obj_from_cache)
        return None

    @staticmethod
    def add_item(id: str, data: SubmenuObj) -> None:
        r.json().set(id, '$', data.model_dump())

    def update_submenu_count(self, id: str, incr: int) -> None:
        if r.exists(id):
            r.json().numincrby(id, Path(self.path), incr)


submenu_cache = CacheSubmenu('.submenus_count')
