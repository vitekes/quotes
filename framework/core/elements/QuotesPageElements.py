# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from framework.core.lib.WebDriverExt import WebDriverExt
from grab import Grab


class QuotesPageElements:
    def __init__(self, driver, config):
        self.base = WebDriverExt(driver)
        self.driver = driver
        self.config = config
        ###########################################LOCATORS###########################################
        self.new_element_added = lambda text: (".//*[@id='tbl']/tbody/tr[last()]//*[text()='{text}']".format(text=text),
                                                     By.XPATH)
        self.new_element_name_added = lambda text: (".//*[@id='tbl']/tbody/tr[last()]//td[1][text()='{text}']".format(text=text),
                                                     By.XPATH)
        self.new_element_count_added = lambda text: (".//*[@id='tbl']/tbody/tr[last()]//td[2][text()='{text}']".format(text=text),
                                                     By.XPATH)
        self.new_element_price_added = lambda text: (".//*[@id='tbl']/tbody/tr[last()]//td[3][text()='{text}']".format(text=text),
                                                     By.XPATH)
        self.quotes_link_add_new = ("open", By.ID)
        self.quotes_name_add_new = ("name", By.ID)
        self.quotes_count_add_new = ("count", By.ID)
        self.quotes_price_add_new = ("price", By.ID)
        self.quotes_button_add_new = ("add", By.ID)

        self.quotes_table = ("tbl", By.ID)
        self.quotes_table_head = (".//*[@id='tbl']//th", By.XPATH)
        self.quotes_table_rows = (".//*[@id='tbl']//tbody/tr", By.XPATH)
        self.quotes_table_cells = (".//*[@id='tbl']/tbody/tr[1]/td", By.XPATH)
        self.quotes_table_head_current = lambda cnt: (".//*[@id='tbl']//th[{cnt}]".format(cnt=str(cnt)), By.XPATH)
        # self.quotes_table_row_current = lambda cnt: (".//*[@id='tbl']//tbody/tr[{cnt}]".format(cnt=str(cnt)), By.XPATH)
        self.quotes_table_cell_current = lambda row, cell: (".//*[@id='tbl']//tbody/tr[{row}]/td[{cell}]"
                                                            .format(row=str(row), cell=str(cell)), By.XPATH)
        self.quotes_table_body_last_element = (".//*[@id='tbl']/tbody/tr[last()]", By.XPATH)
        ###########################################LOCATORS###########################################

    def click_show_add_element_section(self):
        self.base.click_element(element=self.quotes_link_add_new)

    def wait_add_element_section(self):
        self.base.wait_element(element=self.quotes_button_add_new)

    def input_item_name(self, name):
        self.base.input_text(element=self.quotes_name_add_new, text=name)

    def input_item_count(self, count):
        self.base.input_text(element=self.quotes_count_add_new, text=count)

    def input_item_price(self, price):
        self.base.input_text(element=self.quotes_price_add_new, text=price)

    def click_add_item_button(self):
        self.base.click_element(element=self.quotes_button_add_new)

    def wait_element_added(self, text):
        self.base.wait_element(element=self.new_element_added(text=text))

    def get_table_body_text(self):
        body = []
        rows = self.base.get_elements_count(element=self.quotes_table_rows)
        if rows > 0:
            cells = self.base.get_elements_count(element=self.quotes_table_cells)
        else:
            return []
        for row in xrange(1, len(rows)+1):
            current_row = []
            for cell in xrange(1, len(cells)):
                current_row.append(self.base.get_element_text(element=self.quotes_table_cell_current(row=row,
                                                                                                     cell=cell)))
            body.append(current_row)
        return body

    def is_data_added_correctly(self, name, count, price):
        assert_items = [False, False, False]
        assert_items[0] = self.base.wait_element(
            element=self.new_element_name_added(name),
            timeout=3
        )
        assert_items[1] = self.base.wait_element(
            element=self.new_element_count_added(count),
            timeout=3
        )
        assert_items[2] = self.base.wait_element(
            element=self.new_element_price_added(price),
            timeout=3
        )
        return assert_items

########################################### USE GRAB ###########################################

    def grab_get_table_body_text(self, url):  # TODO: Rewrite human way
        page = Grab()
        page.go(url)

        body = []
        rows =  page.doc.select(self.quotes_table_rows[0]).count()
        if rows > 0:
            cells = page.doc.select(self.quotes_table_cells[0]).count() - 1 # Ignore last collumn
        else:
            return []
        for row in xrange(1, rows):
            current_row = []
            for cell in xrange(1, cells):
                current_row.append(page.doc.select(self.quotes_table_cell_current(row=row,cell=cell)[0]).text())
            body.append(current_row)
        return body