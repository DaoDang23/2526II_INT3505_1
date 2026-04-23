import os
from pymongo import MongoClient

def get_db():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("DB_NAME", "soa_product_db")
    client = MongoClient(uri)
    return client[db_name]