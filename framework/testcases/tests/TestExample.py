# -*- coding: utf-8 -*-
from framework.core.lib.DriverManager import DriverManager
from framework.core.lib.GlobalManager import GlobalManager


class TestExample:
######################################SETUP AND TEARDOWN###############################################
    def setup_class(self):
        self.driver = DriverManager().driver
        self.manager = GlobalManager(self.driver)
        self.data = self.manager.config
        self.driver.maximize_window()

    def setup(self):
        url = self.data["url"] + "/auth/login/"
        self.driver.get(url)

##########################################TESTCASES####################################################

    def test_example1(self):
        pass

    def test_example2(self):
        pass

    def test_example3(self):
        pass

###########################################TEARDOWN#####################################################
    def teardown(self):
        if self.manager.auth.main_menu_present():
            self.manager.auth.logout()

    def teardown_class(self):
        self.driver.quit()
