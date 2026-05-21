from flask import Blueprint, jsonify, request

from models import books, members, borrow_records
from utils import paginate, search_books

library_bp = Blueprint("library", __name__)


@library_bp.route("/")
def home():
    return jsonify({
        "message": "Week5 Library API",
        "docs": "/apidocs"
    })


@library_bp.route("/books", methods=["GET"])
def get_books():
    """
    Get all books with pagination
    ---
    tags:
      - Books
    parameters:
      - name: page
        in: query
        type: integer
      - name: limit
        in: query
        type: integer
    responses:
      200:
        description: List books
    """

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 2))

    result = paginate(books, page, limit)

    return jsonify(result)


@library_bp.route("/books/search", methods=["GET"])
def find_books():
    """
    Search books
    ---
    tags:
      - Books
    parameters:
      - name: keyword
        in: query
        type: string
    responses:
      200:
        description: Search result
    """

    keyword = request.args.get("keyword", "")

    result = search_books(books, keyword)

    return jsonify(result)


@library_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """
    Get book detail
    ---
    tags:
      - Books
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Book detail
      404:
        description: Book not found
    """

    for book in books:
        if book["id"] == book_id:
            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404


@library_bp.route("/members", methods=["GET"])
def get_members():
    """
    Get all members
    ---
    tags:
      - Members
    responses:
      200:
        description: List members
    """

    return jsonify(members)


@library_bp.route("/members/<int:member_id>/borrowed-books", methods=["GET"])
def borrowed_books(member_id):
    """
    Resource Tree Example
    ---
    tags:
      - Members
    parameters:
      - name: member_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Borrowed books
    """

    result = []

    for record in borrow_records:
        if record["member_id"] == member_id:

            for book in books:
                if book["id"] == record["book_id"]:
                    result.append(book)

    return jsonify({
        "member_id": member_id,
        "borrowed_books": result
    })