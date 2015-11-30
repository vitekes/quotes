# -*- coding: utf-8 -*-
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from allure.constants import AttachmentType
import types
import allure
import pytest
import logging

logging.basicConfig(level=logging.INFO)

def log_wrapper(fn):
        tmp = fn.__name__
        log = logging.getLogger("{}".format(tmp))
        def wrapper(self, *args, **kwargs):
            log.info("start method ")
            fn(self, *args, **kwargs)
            log.info("finish method")
        return wrapper


class WebDriverExt:
    def __init__(self, driver):
        self.driver = driver
        self._instance = self
    ### __init__

    @allure.step("Нажатие на элемент: {element}")
    def click_element(self, element=None):
        locator, _type = element

        wait_res = self.wait_element(element)
        if not wait_res:
            allure.attach('screenshot', self.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
            pytest.fail("element {} not found".format(locator))

        self.driver.find_element(by=_type, value=locator).click()
    ### click_element

    @allure.step("Очищаем текстовое поле: {element}")
    def clear_field(self, element=None):
        if isinstance(element, types.DictType):
            element = element['element']
        locator, _type = element

        if not self.wait_element(element):
            allure.attach('screenshot', self.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
            pytest.fail("element {} not found".format(locator))
        self.driver.find_element(by=_type, value=locator).clear()
    ### clear_field

    @allure.step("Ввод текста {text} в текстовое поле: {element}")
    def input_text(self, element=None, text=''):
        locator, _type = element
        if not self.wait_element(element):
            allure.attach('screenshot', self.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
            pytest.fail("element {} not found".format(locator))
        self.driver.find_element(by=_type, value=locator).clear()
        self.driver.find_element(by=_type, value=locator).send_keys(text.decode('utf-8'))
    ### input_text

    @allure.step("Выбираем элемент {value} из списка: {element}")
    def select_from_list(self, element=None, value=None):
        locator, _type = element
        if not self.wait_element(element):
            allure.attach('screenshot', self.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
            pytest.fail("element {} not found".format(locator))
        select = Select(self.driver.find_element(by=_type, value=locator))
        select.select_by_value(value)

    @allure.step("Выбираем элемент из списка по введённому имени {name}: {element}")
    def select_element_by_name(self, element=None, name=None):
        locator, _type = element
        self.input_text(element=element, text=name)
        self.driver.find_element(by=_type, value=locator).send_keys(Keys.RETURN)

    # select visible element
    @allure.step("Выбираем элемент из списка : {element}")
    def select_visible_element(self, element=None, name=None):
        locator, _type = element
        self.driver.find_element(by=_type, value=locator).click()

    @allure.step("Получаем текст элемента : {element}")
    def get_element_text(self, element=None):
        locator, _type = element
        return self.driver.find_element(by=_type, value=locator).text

    @allure.step("Получаем количество элементов удовлетворяющих значению: {element}")
    def get_elements_count(self, element=None):
        locator, _type = element
        return self.driver.find_elements(by=_type, value=locator)

    @allure.step("Ожидание элемента")
    def wait_element(self, element=None, timeout=30, xfail=False, locator=None):
        log = logging.getLogger("{}".format("wait_element"))
        locator, _type = element
        # allure.step("максимальное время ожидания элемента - {timeout}")
        try:
            WebDriverWait(self.driver, timeout).until(lambda find: find.find_element(_type, locator))
            log.info("element {} found".format(locator))
            return True
        except TimeoutException:
            if xfail:
                pytest.fail("element {} not found".format(locator))
            else:
                log.error("element {} not found".format(locator))
            return False
    ### wait_element

    @allure.step("Проверка присутствуя элемента: {element}")
    def is_element_present(self, element=None):
        log = logging.getLogger("{}".format("is_element_present"))
        locator, _type = element
        try:
           self.driver.find_element(by=_type, value=locator)
           log.info("element {} present".format(locator))
        except NoSuchElementException, e:
            allure.attach('screenshot', self.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
            log.error("element {} not present".format(locator))
            return False
        return True
    ### is_element_present
