from framework.core.lib.ConfigManager import ConfigManager
from framework.core.steps.QuotesSteps import QuotesSteps
from pymongo import MongoClient

class GlobalManager:
    def __init__(self, driver=None):
        ######################init config##########################
        filename = "framework/testcases/testdata/testdata.yaml" # TODO load file from command line
        cfg = ConfigManager()
        self.config = cfg.config_load(filename=filename)["params"]
        ###########################################################
        client = MongoClient(self.config["dbhost"], self.config["dbport"])
        self.db = client[self.config["dbname"]]
        self.qoutes = QuotesSteps(driver, self.config, self.db)
