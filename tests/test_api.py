import json
from uuid import uuid4

from requests import get, post, patch, delete
from re import compile
import pytest


def get_menus(self):
    response = get(f'{self.url}')
    assert response.status_code == 200
    assert response.text[0] == '[' and response.text[-1] == ']'


def get_menu_item(self):
    response = get(self.url+self.main_menu_id)

    if response.status_code == 200:
        pattern = compile(f'{{"id":"{self.main_menu_id}",'
                          f'"title":"{self.menu_title}",'
                          f'"description":"{self.menu_description}",'
                          f'"submenus_count":{self.get_submenus_count()},'
                          f'"dishes_count":{self.get_count_dishes_in_menu()}}}')

        assert response.headers['content-type'] == 'application/json'
        assert response.status_code == 200
        assert pattern.match(response.text)

    elif response.status_code == 404:
        pattern = compile('{"detail":"menu not found"}')

        assert response.headers['content-type'] == 'application/json'
        assert response.status_code == 404
        assert pattern.match(response.text)


def post_menu(self):
    response = post(self.url,
                    data=json.dumps({
                        "id": self.main_menu_id,
                        "title": self.menu_title,
                        "description": self.menu_description
                    }))

    self.items_count[self.main_menu_id] = dict()

    pattern = compile(f'{{"id":"{self.main_menu_id}",'
                        f'"title":"{self.menu_title}",'
                        f'"description":"{self.menu_description}",'
                        f'"submenus_count":{self.get_submenus_count()},'
                        f'"dishes_count":{self.get_count_dishes_in_menu()}}}')

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 201
    assert pattern.match(response.text)


def update_menu(self):
    TestMenu.title = self.menu_updated_title
    TestMenu.description = self.menu_updated_description

    response = patch(url=self.url + self.main_menu_id, data=json.dumps({
        "title": self.menu_title,
        "description": self.menu_description
    }))

    pattern = compile(f'{{"id":"{self.main_menu_id}",'
                        f'"title":"{self.menu_title}",'
                        f'"description":"{self.menu_description}",'
                        f'"submenus_count":{self.get_submenus_count()},'
                        f'"dishes_count":{self.get_count_dishes_in_menu()}}}')

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 200
    assert pattern.match(response.text)


def delete_menu(self):
    pattern = compile('{"status":true,'
                      '"message":"The menu has been deleted"}')

    response = delete(url=self.url + self.main_menu_id)

    if response.status_code == 200:
        self.items_count.pop(self.main_menu_id)

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 200
    assert pattern.match(response.text)


# SUBMENUS TESTS ###############################################################

def get_submenus(self):
    response = get(url=self.sub_menu_url)
    assert response.status_code == 200
    assert response.text[0] == '[' and response.text[-1] == ']'


def post_submenu(self):
    response = post(url=self.sub_menu_url,
                    data=json.dumps({
                        "id": self.sub_menu_id,
                        "title": self.submenu_title,
                        "description": self.submenu_description
                    }))
    if response.status_code == 201:
        if self.sub_menu_id not in self.items_count[self.main_menu_id]:
            self.items_count[self.main_menu_id][self.sub_menu_id] = []

    pattern = compile(f'{{"id":"{self.sub_menu_id}",'
                        f'"title":"{self.submenu_title}",'
                        f'"description":"{self.submenu_description}",'
                        f'"dishes_count":{self.get_count_dishes_in_submenu()}')

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 201
    assert pattern.match(response.text)


def get_submenu_item(self):
    response = get(self.sub_menu_url + self.sub_menu_id)

    if response.status_code == 200:
        pattern = compile(f'{{"id":"{self.sub_menu_id}",'
                          f'"title":"{self.submenu_title}",'
                          f'"description":"{self.submenu_description}",'
                          f'"dishes_count":{self.get_count_dishes_in_submenu()}')

        assert response.headers['content-type'] == 'application/json'
        assert response.status_code == 200
        assert pattern.match(response.text)

    elif response.status_code == 404:
        pattern = compile('{"detail":"submenu not found"}')

        assert response.headers['content-type'] == 'application/json'
        assert response.status_code == 404
        assert pattern.match(response.text)


def update_submenu(self):
    TestSubmenu.submenu_title = self.submenu_updated_title
    TestSubmenu.submenu_description = self.submenu_updated_description
    pattern = compile(f'{{"id":"{self.sub_menu_id}",'
                      f'"title":"{self.submenu_title}",'
                      f'"description":"{self.submenu_description}",'
                      f'"dishes_count":{self.get_count_dishes_in_submenu()}')

    response = patch(url=self.sub_menu_url + self.sub_menu_id, data=json.dumps({
        "title": self.submenu_title,
        "description": self.submenu_description
    }))

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 200
    assert pattern.match(response.text)


def delete_submenu(self):
    pattern = compile('{"status":true,'
                      '"message":"The menu has been deleted"}')

    response = delete(url=self.sub_menu_url + self.sub_menu_id)
    if response.status_code == 200:
        self.items_count[self.main_menu_id].pop(self.sub_menu_id)

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 200
    assert pattern.match(response.text)

# DISHES TESTS #################################################################


def get_dishes(self):
    response = get(url=self.dish_url)
    assert response.status_code == 200
    assert response.text[0] == '[' and response.text[-1] == ']'


def post_dish(self):

    response = post(url=self.dish_url,
                    data=json.dumps({
                        "id": self.dish_id,
                        "title": self.dish_title,
                        "description": self.dish_description,
                        "price": self.price
                    }))


    self.items_count[self.main_menu_id][self.sub_menu_id].append(self.dish_id)

    pattern = compile(f'{{"id":"{self.dish_id}",'
                        f'"title":"{self.dish_title}",'
                        f'"description":"{self.dish_description}",'
                        f'"price":"{self.price}"')

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 201
    assert pattern.match(response.text)


def get_dish_item(self):
    response = get(self.dish_url + self.dish_id)

    if response.status_code == 200:
        pattern = compile(f'{{"id":"{self.dish_id}",'
                          f'"title":"{self.dish_title}",'
                          f'"description":"{self.dish_description}",'
                          f'"price":"{self.price}"')

        assert response.headers['content-type'] == 'application/json'
        assert response.status_code == 200
        assert pattern.match(response.text)

    elif response.status_code == 404:
        pattern = compile('{"detail":"dish not found"}')

        assert response.headers['content-type'] == 'application/json'
        assert response.status_code == 404
        assert pattern.match(response.text)


def update_dish(self):
    TestDish.title = self.dish_updated_title
    TestDish.description = self.dish_updated_description
    TestDish.price = self.updated_price
    pattern = compile(f'{{"id":"{self.dish_id}",'
                      f'"title":"{self.dish_title}",'
                      f'"description":"{self.dish_description}",'
                      f'"price":"{self.price}"')

    response = patch(url=self.dish_url + self.dish_id, data=json.dumps({
        "title": self.dish_title,
        "description": self.dish_description,
        "price": self.price
    }))

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 200
    assert pattern.match(response.text)


def delete_dish(self):
    pattern = compile('{"status":true,'
                      '"message":"The menu has been deleted"}')

    response = delete(url=self.dish_url + self.dish_id)
    if response.status_code == 200:
        self.items_count[self.main_menu_id][self.sub_menu_id].remove(self.dish_id)

    assert response.headers['content-type'] == 'application/json'
    assert response.status_code == 200
    assert pattern.match(response.text)


# TEST CLASSES #################################################################


@pytest.mark.usefixtures('set_test_menu_variables')
class TestMenu:
    test_get_menus_1 = get_menus
    test_post_menu = post_menu
    test_get_menus_2 = get_menus
    test_get_menu_item_1 = get_menu_item
    test_update_menu = update_menu
    test_get_menu_item_2 = get_menu_item
    test_delete_menu = delete_menu
    test_get_menus_3 = get_menus
    test_get_menu_item_3 = get_menu_item


@pytest.mark.usefixtures('set_test_menu_variables')
class TestSubmenu:
    test_post_menu = post_menu
    test_get_submenus_1 = get_submenus
    test_post_submenu = post_submenu
    test_get_submenus_2 = get_submenus
    test_get_submenu_item_1 = get_submenu_item
    test_update_submenu = update_submenu
    test_get_submenu_item_2 = get_submenu_item
    test_delete_submenu = delete_submenu
    test_get_submenus_3 = get_submenus
    test_get_submenu_item_3 = get_submenu_item
    test_delete_menu = delete_menu
    test_get_menus = get_menus


@pytest.mark.usefixtures('set_test_menu_variables')
class TestDish:
    test_post_menu = post_menu
    test_post_submenu = post_submenu
    test_get_dishes_1 = get_dishes
    test_post_dish = post_dish
    test_get_dishes_2 = get_dishes
    test_get_dish_item_1 = get_dish_item
    test_update_dish = update_dish
    test_get_dish_item_2 = get_dish_item
    test_delete_dish = delete_dish
    test_get_dishes_3 = get_dishes
    test_get_dish_item_3 = get_dish_item
    test_delete_submenu = delete_submenu
    test_get_submenus = get_submenus
    test_delete_menu = delete_menu
    test_get_menus = get_menus


@pytest.mark.usefixtures('set_test_menu_variables')
class TestDishesCount:
    test_post_menu = post_menu
    test_post_submenu = post_submenu
    test_post_dish_1 = post_dish

    def test_set_dish_2(self):
        TestDishesCount.dish_id = str(uuid4())
        TestDishesCount.dish_title = 'My dish 2'
        TestDishesCount.dish_description = 'My dish description 2'

    test_post_dish_2 = post_dish
    test_get_menu_item_1 = get_menu_item
    test_get_submenu_item = get_submenu_item
    test_delete_submenu = delete_submenu
    test_get_submenus = get_submenus
    test_get_dishes = get_dishes
    test_get_menu_item_2 = get_menu_item
    test_delete_menu = delete_menu
    test_get_menus = get_menus
