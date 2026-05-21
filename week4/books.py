from flask import Blueprint, jsonify, request

books_bp = Blueprint('books', __name__)

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "price": 29.99
    }
]

@books_bp.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404

@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
        "price": data["price"]
    }

    books.append(new_book)

    return jsonify(new_book), 201

@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()

    for book in books:
        if book["id"] == book_id:
            book["title"] = data["title"]
            book["author"] = data["author"]
            book["price"] = data["price"]

            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return jsonify({
                "message": "Book deleted successfully"
            })

    return jsonify({"error": "Book not found"}), 404