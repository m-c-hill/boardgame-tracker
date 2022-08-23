from flask import request


def paginate_questions(request: request, items: list, items_per_page: int):
    """
    Return paginated list of items from requested page number.
    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    formatted_questions = [item.format() for item in items]

    return formatted_questions[start:end]
