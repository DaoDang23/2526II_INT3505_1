from bson.objectid import ObjectId
from src.config.db import get_db
from src.models.product import serialize_product

def get_collection():
    db = get_db()
    return db["products"]

def get_all_products():
    products = get_collection().find()
    return [serialize_product(p) for p in products]

def get_product_by_id(product_id):
    product = get_collection().find_one({"_id": ObjectId(product_id)})
    return serialize_product(product)

def create_product(product_data):
    result = get_collection().insert_one(product_data)
    product_data["_id"] = result.inserted_id
    return serialize_product(product_data)

def update_product(product_id, update_data):
    result = get_collection().update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    if result.matched_count > 0:
        return get_product_by_id(product_id)
    return None

def delete_product(product_id):
    result = get_collection().delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0