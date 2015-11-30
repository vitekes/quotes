# -*- coding: utf-8 -*-
from framework.core.lib.GlobalManager import GlobalManager

class TestNoWebdriver:
######################################SETUP AND TEARDOWN###############################################
    def setup_class(self):
        self.manager = GlobalManager()
        self.data = self.manager.config

##########################################TESTCASES####################################################

    def test_download_data_from_table(self):
        data = self.manager.qoutes.grab_get_data_from_table(self.data["url"])
        self.manager.qoutes.add_data_to_db(query_list=data, collection=self.data["dbcollection"])
        self.manager.qoutes.compare_db_and_table(collection=self.data["dbcollection"])
        assert self.manager.qoutes.db_not_empty(collection=self.data["dbcollection"])

###########################################TEARDOWN#####################################################
    def teardown(self):
        self.manager.qoutes.remove_collection(collection=self.data["dbcollection"])