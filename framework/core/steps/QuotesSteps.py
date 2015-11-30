# -*- coding: utf-8 -*-
import allure
import json
from framework.core.elements.QuotesPageElements import QuotesPageElements


class QuotesSteps:
    def __init__(self, driver, config, db_instance):
        self.qElements = QuotesPageElements(driver, config)
        self.config = config
        self.db = db_instance

    @allure.step("Собрать данные из таблицы")
    def get_data_from_table(self):
        collected_data = []
        head = ["name", "count", "price"]
        body = self.qElements.get_table_body_text()
        for body_item in body:
            collected_data.append(dict(zip(head, body_item)))
        return collected_data

    @allure.step("Добавить данные в таблицу")
    def add_item_to_table(self, item_name, item_count, item_price):
        self.qElements.click_show_add_element_section()
        self.qElements.wait_add_element_section()
        self.qElements.input_item_name(item_name)
        self.qElements.input_item_count(item_count)
        self.qElements.input_item_price(item_price)
        self.qElements.click_add_item_button()
        self.qElements.wait_element_added(item_name)

    @allure.step("Проверить что данные добавлены корректно")
    def assert_items_added(self, name, count, price):

        msg = lambda collumn, value: "Значение в столбце {collumn} не совпадает с ожидаемым значением {value}::".format(
                                                                                                        collumn=collumn,
                                                                                                        value=value)
        assert_msg = "Проверка значений: "
        fail_count = 0
        assert_list = self.qElements.is_data_added_correctly(name, count, price)
        if not assert_list[0]:
            assert_msg += msg(collumn='Название', value=name)
            fail_count +=1
        if not assert_list[1]:
            assert_msg += msg(collumn='Количество', value=str(count))
            fail_count +=1
        if not assert_list[2]:
            assert_msg += msg(collumn='стоимость', value=str(price))
            fail_count +=1

        if fail_count > 0:
            return False, assert_msg
        return True, assert_msg + "Все значения добавлены корректно"

    @allure.step("Сравнить данные")
    def compare_db_and_table(self, collection):
        page_data = self.get_data_from_table()
        db_data = self.get_data_from_db(collection)
        result = self.compare_values(page_data, db_data)
        if result['deleted']:
            allure.step(
                "Удалены строки: collumn={deleted_name}, count={deleted_count}, price={deleted_price}".format(
                    result["deleted"][0]["name"],
                    result["deleted"][0]["count"],
                    result["deleted"][0]["price"]
                )
            )
        if result['added']:
            allure.step(
                "Добавлены строки: collumn={added_name}, count={added_count}, price={added_price}".format(
                    added_name=result["added"][0]["name"],
                    added_count=result["added"][0]["count"],
                    added_price=result["added"][0]["price"]
                )
            )

    @allure.step("Добавить данные в базу данных")
    def add_data_to_db(self, query_list, collection):
        for query in query_list:
            self.db[collection].save(query)

    @allure.step("Проверка того что коллекция не пустая")
    def db_not_empty(self, collection):
        return self.db[collection].count()

    @allure.step("Удаление коллекции")
    def remove_collection(self, collection):
        self.db.drop_collection(collection)

    @allure.step("Запрашиваем данные из коллекции в базе данных")
    def get_data_from_db(self, collection):
        return [item for item in self.db[collection].find()]

    @allure.step("Сравниваем значения в базе и в таблице")
    def compare_values(self, page_data, db_data):
        added = []
        deleted = []
        item_list = {'deleted':[], 'added':[]}
        for db_item in db_data:
             cnt = 0
             for page_item in page_data:
                 if (db_item['name'] == page_item['name'] and
                     db_item['count'] == page_item['count'] and
                     db_item['price'] == page_item['price']):
                     cnt += 1
                     break
             if cnt == 0:
                deleted.append(db_item)

        for page_item in page_data:
            cnt = 0
            for db_item in db_data:
                if (page_item['name'] == db_item['name'] and
                    page_item['count'] == db_item['count'] and
                    page_item['price'] == db_item['price']):
                    cnt += 1
                    break
            if cnt == 0:
                added.append(page_item)
        item_list['deleted'] = deleted
        item_list['added'] = added
        return item_list

########################################### USE GRAB ###########################################
    @allure.step("GRAB: Собрать данные из таблицы")
    def grab_get_data_from_table(self, url):
        collected_data = []
        head = ["name", "count", "price"]
        body = self.qElements.grab_get_table_body_text(url)
        for body_item in body:
            collected_data.append(dict(zip(head, body_item)))
        return collected_data