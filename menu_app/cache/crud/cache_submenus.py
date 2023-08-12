from redis.commands.json.path import Path

from menu_app.cache.cache import r
from menu_app.cache.crud.cache_base import CacheBase


class CacheSubmenu(CacheBase):
    def update_submenu_count(self, id: str, incr: int) -> None:
        if r.exists(id):
            r.json().numincrby(id, Path(self.path), incr)


submenu_cache = CacheSubmenu('.submenus_count')
