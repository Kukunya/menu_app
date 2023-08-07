from os import environ
from uuid import uuid4

import pytest
from sqlalchemy import create_engine

from menu_app.core.config import SQLALCHEMY_DATABASE_URI

APP_HOST = environ.get('REDIS_URI')

TEST_ENGINE = create_engine(SQLALCHEMY_DATABASE_URI.unicode_string())


@pytest.fixture(scope='class', autouse=True)
def set_test_menu_variables(request):
    request.cls.url = f'http://{APP_HOST}:8000/api/v1/menus/'
    request.cls.main_menu_id = str(uuid4())
    request.cls.menu_title = 'My menu 1'
    request.cls.menu_description = 'My menu description 1'
    request.cls.menu_updated_title = 'My updated menu 1'
    request.cls.menu_updated_description = 'My updated menu description 1'
    request.cls.sub_menu_url = f'{request.cls.url}{request.cls.main_menu_id}/submenus/'
    request.cls.sub_menu_id = str(uuid4())
    request.cls.submenu_title = 'My submenu 1'
    request.cls.submenu_description = 'My submenu description 1'
    request.cls.submenu_updated_title = 'My updated submenu 1'
    request.cls.submenu_updated_description = 'My updated submenu description 1'
    request.cls.dish_url = f'{request.cls.sub_menu_url}{request.cls.sub_menu_id}/dishes/'
    request.cls.dish_id = str(uuid4())
    request.cls.dish_title = 'My dish 1'
    request.cls.dish_description = 'My dish description 1'
    request.cls.price = '12.50'
    request.cls.dish_updated_title = 'My updated dish 1'
    request.cls.dish_updated_description = 'My updated dish description 1'
    request.cls.updated_price = '14.50'
    request.cls.items_count = dict()
    request.cls.get_submenus_count = lambda self: len(self.items_count[self.main_menu_id])
    request.cls.get_count_dishes_in_submenu = lambda self: len(self.items_count[self.main_menu_id][self.sub_menu_id])
    request.cls.get_count_dishes_in_menu = lambda self: len(
        [i for i in self.items_count[self.main_menu_id].values()][0]
    ) if self.get_submenus_count() else 0


@pytest.fixture(scope='class', autouse=True)
def set_dish_1(request):
    request.cls.dish_title = 'My dish 1'
    request.cls.dish_description = 'My dish description 1'


@pytest.fixture(scope='class', autouse=True)
def set_dish_2(request):
    request.cls.dish_id = str(uuid4())
    request.cls.dish_title = 'My dish 2'
    request.cls.dish_description = 'My dish description 2'
