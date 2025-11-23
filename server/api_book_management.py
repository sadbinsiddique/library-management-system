# file: server/api_book_management.py
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

BOOK_FILE = "database/books.txt"

class BookModel(BaseModel):
    title: str
    author: str
    isbn: str 
    published_year: int
    copies_available: int

# Update Base Model (BUG)
class BookUpdate(BaseModel): 
    title: str = None
    author: str = None
    isbn: str = None
    published_year: int = None
    copies_available: int = None

def ensure_database_directory():
    os.makedirs("database", exist_ok=True)
    if not os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, 'w') as f:
            pass

def get_next_book_id():
    ensure_database_directory()
    max_id = 0

    if os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    book_id = int(line.split('|')[0])
                    max_id = max(max_id, book_id)

    return max_id + 1

@app.get("/", response_model=dict, status_code=200)
async def get_all_books():
    ensure_database_directory()
    books = {}

    with open(BOOK_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                book_id = parts[0]
                books[book_id] = {
                    "title": parts[1],
                    "author": parts[2],
                    "isbn": parts[3],
                    "published_year": int(parts[4]),
                    "copies_available": int(parts[5])
                }

    return books

@app.post("/", response_model=dict, status_code=201)
async def add_book(book: BookModel):
    ensure_database_directory()
    
    # Check for duplicate ISBN
    if os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if parts[3] == book.isbn:
                        raise HTTPException(
                            status_code=409, 
                            detail="\n--------- Book with this ISBN already exists ---------\n"
                        )
                    
    book_id = get_next_book_id()

    with open(BOOK_FILE, 'a') as f:
        book_record = f"{book_id}|{book.title}|{book.author}|{book.isbn}|{book.published_year}|{book.copies_available}\n"
        f.write(book_record)
    
    return {
        "id": book_id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "published_year": book.published_year,
        "copies_available": book.copies_available
    }

@app.get("/{book_id}", response_model=dict, status_code=200)
async def get_book_by_id(book_id: int):
    ensure_database_directory()

    if not os.path.exists(BOOK_FILE):
        raise HTTPException(
            status_code=404, 
            detail="\n-------- Book not found --------\n"
        )
    
    with open(BOOK_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == book_id:
                    return {
                        "title": parts[1],
                        "author": parts[2],
                        "isbn": parts[3],
                        "published_year": int(parts[4]),
                        "copies_available": int(parts[5])
                    }
                
    raise HTTPException(
        status_code=404, 
        detail="\n-------- Book not found --------\n"
    )

@app.put("/{book_id}", response_model=dict, status_code=200)
async def update_book_by_id(book_id: int, book_update: BookUpdate):
    ensure_database_directory()
    
    books = []
    book_found = False
    updated_book = None

    if not os.path.exists(BOOK_FILE):
        raise HTTPException(
            status_code=404, 
            detail="\n-------- Book not found --------\n"
        )

    with open(BOOK_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')

                if int(parts[0]) == book_id:
                    book_found = True

                    # update only the provided fields
                    title = book_update.title if book_update.title is not None else parts[1]
                    author = book_update.author if book_update.author is not None else parts[2]
                    isbn = book_update.isbn if book_update.isbn is not None else parts[3]
                    published_year = book_update.published_year if book_update.published_year is not None else int(parts[4])
                    copies_available = book_update.copies_available if book_update.copies_available is not None else int(parts[5])

                    updated_line = f"{book_id}|{title}|{author}|{isbn}|{published_year}|{copies_available}\n"
                    books.append(updated_line)

                    updated_book = {
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                        "published_year": published_year,
                        "copies_available": copies_available
                    }
                else:
                    books.append(line)

    if not book_found:
        raise HTTPException(
            status_code=404, 
            detail="\n-------- Book not found --------\n"
        )

    with open(BOOK_FILE, 'w') as f:
        f.writelines(books)

    return updated_book

@app.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int):
    ensure_database_directory()
    
    books = []
    book_found = False

    if not os.path.exists(BOOK_FILE):
        raise HTTPException(
            status_code=404, 
            detail="\n-------- Book not found --------\n"
        )

    with open(BOOK_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')

                if int(parts[0]) == book_id:
                    book_found = True
                else:
                    books.append(line)

    if not book_found:
        raise HTTPException(
            status_code=404, 
            detail="\n-------- Book not found --------\n"
        )

    with open(BOOK_FILE, 'w') as f:
        f.writelines(books)

    return None