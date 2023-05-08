from pymongo import MongoClient
from pymongo.database import Database

from pymongo.cursor import Cursor


class MongoDB:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client: MongoClient = None
        self.db: Database = None

    def connect(self) -> None:
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def insert(self, collection: str, data: dict) -> None:
        self.db[collection].insert_one(data)

    def find(self, collection: str, query: dict, **kwargs) -> Cursor:
        return self.db[collection].find_one(query, **kwargs)

    def update(self, collection: str, query: dict, data: dict) -> None:
        self.db[collection].update_one(query, data)

    def delete(self, collection: int, query: dict) -> None:
        self.db[collection].delete_one(query)

    def close(self) -> None:
        self.client.close()
