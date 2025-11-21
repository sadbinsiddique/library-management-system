from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

book_db = {
    1: {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "published_year": 1949,
        "copies_available": 4,
    },
    2: {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "9780060935467",
        "published_year": 1960,
        "copies_available": 2,
    },
    3: {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "published_year": 1925,
        "copies_available": 5,
    },
    4: {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "isbn": "9780141439518",
        "published_year": 1813,
        "copies_available": 3,
    },
    5: {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "isbn": "9780316769488",
        "published_year": 1951,
        "copies_available": 6,
    },
    6: {
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "isbn": "9781503280786",
        "published_year": 1851,
        "copies_available": 2,
    },
    7: {
        "title": "War and Peace",
        "author": "Leo Tolstoy",
        "isbn": "9780199232765",
        "published_year": 1869,
        "copies_available": 3,
    },
    8: {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "isbn": "9780547928227",
        "published_year": 1937,
        "copies_available": 5,
    },
    9: {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "isbn": "9780060850524",
        "published_year": 1932,
        "copies_available": 4,
    },
    10: {
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "isbn": "9780486415871",
        "published_year": 1866,
        "copies_available": 2,
    },
    11: {
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "isbn": "9780261102385",
        "published_year": 1954,
        "copies_available": 3,
    },
    12: {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "isbn": "9780747532699",
        "published_year": 1997,
        "copies_available": 7,
    },
}

class BookModel(BaseModel):
    title: str
    author: str
    isbn: str 
    published_year: int
    copies_available: int

@app.get("/", response_model=dict, status_code=200)
async def get_all_books():
    return {"books": book_db}

@app.post("/", response_model=BookModel, status_code=201)
async def add_book(book: BookModel):
    for existing in book_db.values():
        if existing.get("isbn") == book.isbn:
            raise HTTPException(status_code=409, detail="Book already exists")

    new_id = max(book_db.keys()) + 1 if book_db else 1
    book_db[new_id] = book.model_dump()
    return book_db[new_id]

@app.get("/{book_id}", response_model=BookModel, status_code=200)
async def get_book_by_id(
    book_id: int = Path(..., description="The ID of the book to retrieve")
):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_db[book_id]

@app.put("/{book_id}", response_model=BookModel, status_code=200)
async def update_book(
    book: BookModel, book_id: int = Path(..., description="The ID of the book to update")
):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    book_db[book_id] = book.model_dump()
    return book_db[book_id]

@app.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: int = Path(..., description="The ID of the book to delete")
):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del book_db[book_id]
    return None