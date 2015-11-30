from pymongo import MongoClient


class DBManager:
    def __init__(self, config):
        self.config = config
        client = MongoClient(self.config["host"], config["port"])
        self.db = client.dbname


