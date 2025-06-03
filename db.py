import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient


load_dotenv()

class MongoSingleton:
    _instance: MongoClient = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            uri = os.getenv("MONGODB_URI")
            cls._instance = MongoClient(uri)

        return cls._instance

mongo_client = MongoSingleton.get_client()

database = mongo_client.get_database("yeva_data")
channels_collection = database.get_collection("channels")
menus_collection = database.get_collection("current_menus")
pos_data_collection = database.get_collection("pos_data")
orders_collection = database.get_collection("orders")
