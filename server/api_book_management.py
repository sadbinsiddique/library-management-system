from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from helpers.paths import BOOKS_FILE
from helpers.read_db import load_books
from helpers.write_db import write_records

app = FastAPI()

class BookModel(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    published_year: int | None = None
    available_copies: int | None = None

def load_book_db():
    books = load_books()
    return {book["id"]: book for book in books}

book_db = load_book_db()

@app.get("/", response_model=dict, status_code=200, description="Get all books")
async def get_all_books():
    return book_db

@app.post("/", response_model=BookModel, status_code=201, description="Add a new book")
async def add_book(book: BookModel):
    for existing in book_db.values():
        if existing.get("isbn") == book.isbn:
            raise HTTPException(status_code=409, detail="Conflict")

    new_id = max(book_db.keys()) + 1 if book_db else 1
    book_db[new_id] = book.model_dump()

    rows = [
        f"{bid}|{b['title']}|{b['author']}|{b['isbn']}|{b['published_year']}|{b['available_copies']}"
        for bid, b in book_db.items()
    ]
    write_records(BOOKS_FILE, rows)

    return book_db[new_id]

@app.get("/{book_id}", response_model=BookModel, status_code=200, description="Get a book by ID")
async def get_book_by_id(book_id: int = Path(..., description="The ID of the book to retrieve")):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Not Found")
    return book_db[book_id]

@app.put("/{book_id}", response_model=BookModel, status_code=200, description="Update a book by ID")
async def update_book(book: BookModel, book_id: int = Path(..., description="The ID of the book to update")):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Not Found")

    stored = book_db[book_id]
    stored["title"] = book.title or stored["title"]
    stored["author"] = book.author or stored["author"]
    stored["isbn"] = book.isbn or stored["isbn"]
    stored["published_year"] = book.published_year or stored["published_year"]
    stored["available_copies"] = book.available_copies or stored["available_copies"]

    rows = [
        f"{bid}|{b['title']}|{b['author']}|{b['isbn']}|{b['published_year']}|{b['available_copies']}"
        for bid, b in book_db.items()
    ]
    write_records(BOOKS_FILE, rows)

    return stored

@app.delete("/{book_id}", status_code=204, description="Delete a book by ID")
async def delete_book(book_id: int = Path(..., description="The ID of the book to delete")):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Not Found")

    del book_db[book_id]

    rows = [
        f"{bid}|{b['title']}|{b['author']}|{b['isbn']}|{b['published_year']}|{b['available_copies']}"
        for bid, b in book_db.items()
    ]
    write_records(BOOKS_FILE, rows)

    return None