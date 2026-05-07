from flask import Blueprint, request, jsonify
import src.controllers.product_controller as controller
from bson.errors import InvalidId

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    """
    Lay danh sach tat ca san pham
    ---
    responses:
      200:
        description: A list of products
    """
    return jsonify(controller.get_all_products()), 200

@product_bp.route('/products', methods=['POST'])
def add_product():
    """
    Tao san pham moi
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
            category:
              type: string
            stock:
              type: integer
            imageUrl:
              type: string
    responses:
      201:
        description: San pham da duoc tao
    """
    data = request.json
    new_product = controller.create_product(data)
    return jsonify(new_product), 201

@product_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Lay thong tin san pham theo ID
    ---
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Chi tiet san pham
      404:
        description: Khong tim thay
    """
    try:
        product = controller.get_product_by_id(product_id)
        if product:
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid product ID format"}), 400

@product_bp.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Cap nhat thong tin san pham
    ---
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
    responses:
      200:
        description: San pham da duoc cap nhat
    """
    data = request.json
    try:
        updated_product = controller.update_product(product_id, data)
        if updated_product:
            return jsonify(updated_product), 200
        return jsonify({"error": "Product not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid product ID format"}), 400

@product_bp.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Xoa san pham
    ---
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
    responses:
      204:
        description: Xoa thanh cong
    """
    try:
        if controller.delete_product(product_id):
            return '', 204
        return jsonify({"error": "Product not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid product ID format"}), 400