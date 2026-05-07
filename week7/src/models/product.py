def serialize_product(product_doc):
    if not product_doc:
        return None
    return {
        "id": str(product_doc.get("_id")),
        "name": product_doc.get("name"),
        "description": product_doc.get("description"),
        "price": product_doc.get("price"),
        "category": product_doc.get("category"),
        "stock": product_doc.get("stock"),
        "imageUrl": product_doc.get("imageUrl")
    }