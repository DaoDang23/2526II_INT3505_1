from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Mouse", "price": 50},
]

@app.route("/")
def home():
    return jsonify({"message": "API Running"})


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for product in products:
        if product["id"] == id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


@app.route("/products", methods=["POST"])
def create_product():
    data = request.json

    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"]
    }

    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.json

    for product in products:
        if product["id"] == id:
            product["name"] = data["name"]
            product["price"] = data["price"]

            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    for product in products:
        if product["id"] == id:
            products.remove(product)

            return jsonify({"message": "Deleted successfully"})

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)