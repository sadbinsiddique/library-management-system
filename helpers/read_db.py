from .paths import BOOKS_FILE, USERS_FILE, BORROWS_FILE

def _read_lines(path: str):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def load_books():
    lines = _read_lines(BOOKS_FILE)
    books = []

    for line in lines:
        parts = line.split("|")
        books.append({
            "id": int(parts[0]),
            "title": parts[1],
            "author": parts[2],
            "isbn": parts[3],
            "published_year": int(parts[4]),
            "available_copies": int(parts[5])
        })

    return books

def load_users():
    lines = _read_lines(USERS_FILE)
    users = []

    for line in lines:
        parts = line.split("|")
        users.append({
            "id": int(parts[0]),
            "username": parts[1],
            "full_name": parts[2],
            "email": parts[3],
        })

    return users

def load_borrows():
    lines = _read_lines(BORROWS_FILE)
    borrows = []

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 7:
            continue

        borrows.append({
            "borrow_id": int(parts[0]),
            "user_id": int(parts[1]),
            "book_id": int(parts[2]),
            "borrow_date": parts[3],
            "due_date": parts[4],
            "return_date": parts[5] if parts[5] not in (None, "", "None") else None,
            "status": parts[6]
        })

    return borrows