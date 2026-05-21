def paginate(data, page, limit):
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(data),
        "data": data[start:end]
    }


def search_books(book_list, keyword):
    result = []

    for book in book_list:
        if keyword.lower() in book["title"].lower():
            result.append(book)

    return result