from menu_app.cache.crud.cache_base import CacheBase


class CacheDish(CacheBase):
    pass


dish_cache = CacheDish('.dishes_count')
