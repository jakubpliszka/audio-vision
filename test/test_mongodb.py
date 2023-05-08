import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
from pymongo.errors import ServerSelectionTimeoutError, InvalidOperation
from src.mongodb import MongoDB

# Replace these with your actual MongoDB host, port, and test database name
MONGO_HOST = "localhost"
MONGO_PORT = 27017
TEST_DB_NAME = "test_db"

@pytest.fixture(scope="module")
def mongodb_instance():
    mongodb = MongoDB(MONGO_HOST, MONGO_PORT, TEST_DB_NAME)
    yield mongodb
    mongodb.close()

def test_connect(mongodb_instance: MongoDB):
    try:
        mongodb_instance.connect()
    except ServerSelectionTimeoutError:
        pytest.fail("Failed to connect to MongoDB server")

def test_insert_find(mongodb_instance: MongoDB):
    collection = "test_collection"
    data = {"key": "value"}

    mongodb_instance.insert(collection, data)
    result = mongodb_instance.find(collection, {"key": "value"})

    assert result["key"] == data["key"]

def test_update(mongodb_instance: MongoDB):
    collection = "test_collection"
    query = {"key": "value"}
    new_data = {"$set": {"key": "new_value"}}

    mongodb_instance.update(collection, query, new_data)
    result = mongodb_instance.find(collection, {"key": "new_value"})

    assert result["key"] == "new_value"

def test_delete(mongodb_instance: MongoDB):
    collection = "test_collection"
    query = {"key": "new_value"}

    mongodb_instance.delete(collection, query)
    result = mongodb_instance.find(collection, query)

    assert result is None

def test_close(mongodb_instance: MongoDB):
    mongodb_instance.close()
    with pytest.raises(InvalidOperation):
        mongodb_instance.db.command("ping")
