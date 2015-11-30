# -*- coding: utf-8 -*-
from framework.core.lib.DriverManager import DriverManager
from framework.core.lib.GlobalManager import GlobalManager

class TestLifeCycle:
######################################SETUP AND TEARDOWN###############################################
    def setup_class(self):
        self.driver = DriverManager().driver
        self.manager = GlobalManager(self.driver)
        self.data = self.manager.config
        self.driver.maximize_window()

    def setup(self):
        url = self.data["url"]
        self.driver.page_source.encode("utf-8")
        self.driver.get(url)

##########################################TESTCASES####################################################

    def test_add_new_item(self):
        self.manager.qoutes.add_item_to_table(
            item_name=self.data["item_name"],
            item_count=self.data["item_count"],
            item_price=self.data["item_price"]
        )
        result, msg = self.manager.qoutes.assert_items_added(
            self.data["item_name"],
            self.data["item_count"],
            self.data["item_price"]
        )
        assert result, msg.decode('utf-8')

    def test_download_data_from_table(self):
        data = self.manager.qoutes.get_data_from_table()
        self.manager.qoutes.add_data_to_db(data, collection=self.data["dbcollection"])
        self.manager.qoutes.add_item_to_table(
            item_name=self.data["item_name"],
            item_count=self.data["item_count"],
            item_price=self.data["item_price"]
        )
        self.manager.qoutes.compare_db_and_table(collection=self.data["dbcollection"])
        assert self.manager.qoutes.db_not_empty(collection=self.data["dbcollection"])

###########################################TEARDOWN#####################################################
    def teardown_class(self):
        self.manager.qoutes.remove_collection(collection=self.data["dbcollection"])
        self.driver.quit()
