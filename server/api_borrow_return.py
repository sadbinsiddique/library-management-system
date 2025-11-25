# file: server/api_borrow_return.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import os

app = FastAPI()

class BorrowRequest(BaseModel):
    user_id: int
    book_id: int

class ReturnRequest(BaseModel):
    borrow_id: int

# file paths
BORROWS_FILE = 'database/borrows.txt'
BOOKS_FILE = 'database/books.txt'
USERS_FILE = 'database/users.txt'

def ensure_database_directory():
    os.makedirs("database", exist_ok=True)
    if not os.path.exists(BORROWS_FILE):
        with open(BORROWS_FILE, 'w') as f:
            pass

def get_next_borrow_id():
    ensure_database_directory()
    max_id = 0

    if os.path.exists(BORROWS_FILE):
        with open(BORROWS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    borrow_id = int(line.split('|')[0])
                    if borrow_id > max_id:
                        max_id = borrow_id
    
    return max_id + 1   

def user_exists(user_id):
    if not os.path.exists(USERS_FILE):
        return False
    
    with open(USERS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == user_id: 
                    return True
    return False

def get_book(book_id):
    if not os.path.exists(BOOKS_FILE):
        return None
    
    with open(BOOKS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == book_id:
                    return {
                        'book_id': parts[0],
                        'title': parts[1],
                        'author': parts[2],
                        'isbn': parts[3],
                        'published_year': int(parts[4]),
                        'available_copies': int(parts[5])
                    }
    return None

def update_book_copies(book_id, change):
    if not os.path.exists(BOOKS_FILE):
        return False
    
    books = []
    book_updated = False

    with open(BOOKS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == int(book_id):
                    new_copies = int(parts[5]) + change
                    updated_line = f"{parts[0]}|{parts[1]}|{parts[2]}|{parts[3]}|{parts[4]}|{new_copies}\n"
                    books.append(updated_line)
                    book_updated = True
                else:
                    books.append(line)
    if book_updated:
        with open(BOOKS_FILE, 'w') as f:
            f.writelines(books)
        return True
    return False

@app.post("/borrow", response_model=dict, status_code=201)
async def borrow_book(request: BorrowRequest):
    ensure_database_directory()

    if not user_exists(request.user_id):
        raise HTTPException(
            status_code=404, 
            detail= f"\n ------ User with ID {request.user_id} not found ------ \n"
        )

    book = get_book(request.book_id)
    if not book:
        raise HTTPException(
            status_code=404, 
            detail=f"\n ------ Book with ID {request.book_id} not found ------ \n"
        )
    
    if book['available_copies'] <= 0:
        raise HTTPException(
            status_code=400, 
            detail=f"\n ------ No available copies for Book ID {request.book_id} (All copies are borrowed) ------ \n"
        )

    borrow_id = get_next_borrow_id()
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    with open(BORROWS_FILE, 'a') as f:
        borrow_data = f"{borrow_id}|{request.user_id}|{request.book_id}|{borrow_date}|{due_date}||borrowed\n"
        f.write(borrow_data)

    update_book_copies(request.book_id, -1)

    return {
        "borrow_id": borrow_id,
        "user_id": request.user_id,
        "book_id": request.book_id,
        "book_title": book['title'],
        "borrow_date": borrow_date,
        "due_date": due_date,
        "status": "borrowed",
        "message": f"\n ------ Book ID {request.book_id} successfully borrowed by User ID {request.user_id} ------ \n"
    }

@app.post("/return", response_model=dict, status_code=200)
async def return_book(request: ReturnRequest):
    ensure_database_directory()

    borrows = []
    borrow_found = False
    returned_record = None

    if not os.path.exists(BORROWS_FILE):
        raise HTTPException(
            status_code=404, 
            detail=f"\n ------ No borrow records found ------ \n"
        )

    with open(BORROWS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == request.borrow_id:
                    if parts[6] == "returned":
                        raise HTTPException(
                            status_code=400, 
                            detail=f"\n ------ Borrow record with ID {request.borrow_id} has already been returned ------ \n"
                        )
                    
                    borrow_found = True
                    return_date = datetime.now().strftime("%Y-%m-%d")
                    updated_line = f"{parts[0]}|{parts[1]}|{parts[2]}|{parts[3]}|{return_date}||returned\n"
                    borrows.append(updated_line)

                    returned_record = {
                        "borrow_id": int(parts[0]),
                        "user_id": int(parts[1]),
                        "book_id": int(parts[2]),
                        "borrow_date": parts[3],
                        "due_date": parts[4],
                        "return_date": return_date,
                        "status": "returned"
                    }

                    update_book_copies(int(parts[2]), 1)
                else:
                    borrows.append(line)

    if not borrow_found:
        raise HTTPException(
            status_code=404, 
            detail=f"\n ------ Borrow record with ID {request.borrow_id} not found or already returned ------ \n"
        )

    with open(BORROWS_FILE, 'w') as f:
        f.writelines(borrows)

    return {
        **returned_record,
        "message": f"\n ------ Borrow record ID {request.borrow_id} successfully returned ------ \n"
    }

@app.get("/track/{user_id}", response_model=dict, status_code=200)
async def track_user_borrows(user_id: int):
    ensure_database_directory()

    if not user_exists(user_id):
        raise HTTPException(
            status_code=404, 
            detail=f"\n ------ User with ID {user_id} not found ------ \n"
        )

    user_borrows = []

    if os.path.exists(BORROWS_FILE):
        with open(BORROWS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if int(parts[1]) == user_id:
                        book = get_book(int(parts[2]))
                        user_borrows.append({
                            "borrow_id": int(parts[0]),
                            "book_id": int(parts[2]),
                            "book_title": book["title"] if book else "Unknown",
                            "borrow_date": parts[3],
                            "due_date": parts[4],
                            "return_date": parts[5] if parts[5] else None,
                            "status": parts[6]
                        })
    
    return {
        "user_id": user_id,
        "total_borrows": len(user_borrows),
        "borrows": user_borrows
    }

@app.get("/borrowed-books", response_model=dict, status_code=200)
async def get_all_borrowed_books():
    ensure_database_directory()

    borrowed_books = []

    if os.path.exists(BORROWS_FILE):
        with open(BORROWS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if parts[6] == "borrowed":  # only currently borrowed books
                        book = get_book(int(parts[2]))
                        borrowed_books.append({
                            "borrow_id": int(parts[0]),
                            "user_id": int(parts[1]),
                            "book_id": int(parts[2]),
                            "book_title": book["title"] if book else "Unknown",
                            "borrow_date": parts[3],
                            "due_date": parts[4],
                            "status": parts[6]
                        })
    
    return {
        "total_borrowed": len(borrowed_books),
        "borrowed_books": borrowed_books
    }

@app.get("/check-availability/{book_id}", response_model=dict, status_code=200)
async def check_book_availability(book_id: int):
    ensure_database_directory()

    book = get_book(book_id)
    if not book:
        raise HTTPException(
            status_code = 404, 
            detail=f"\n ------ Book with ID {book_id} not found ------ \n"
        )

    is_available = book['available_copies'] > 0

    return {
        "book_id": book_id,
        "book_title": book["title"],
        "author": book["author"],
        "total_copies": book['available_copies'],
        "is_available": is_available,
        "status": "Available" if is_available else "Not Available"
    }