from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from datetime import datetime, timedelta
from helpers.read_db import load_books, load_users, load_borrows
from helpers.write_db import write_records
from helpers.paths import BOOKS_FILE, BORROWS_FILE

app = FastAPI()

class BorrowReturnModel(BaseModel):
    borrow_id: int | None = None
    user_id: int
    book_id: int
    borrow_date: str | None = None
    due_date: str | None = None
    return_date: str | None = None
    status: str | None = "borrowed"

book_db = {book['id']: book for book in load_books()}
user_db = {user['id']: user for user in load_users()}
borrow_db = {borrow['borrow_id']: borrow for borrow in load_borrows()}

def get_next_borrow_id():
    return max(borrow_db.keys(), default=0) + 1

def update_book_copies(book_id: int, change: int):
    if book_id not in book_db:
        return False
    book_db[book_id]['available_copies'] += change
    rows = [
        f"{b['id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['published_year']}|{b['available_copies']}"
        for b in book_db.values()
    ]
    write_records(BOOKS_FILE, rows)
    return True

def persist_borrows():
    rows = [
        f"{b['borrow_id']}|{b['user_id']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{b['return_date'] or ''}|{b['status']}"
        for b in borrow_db.values()
    ]
    write_records(BORROWS_FILE, rows)

@app.post("/", response_model=BorrowReturnModel, status_code=201, description="Borrow a book")
async def borrow_book(record: BorrowReturnModel):
    if record.user_id not in user_db:
        raise HTTPException(status_code=404, detail="Not Found")
    if record.book_id not in book_db:
        raise HTTPException(status_code=404, detail="Not Found")
    
    book = book_db[record.book_id]
    if book['available_copies'] <= 0:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    for b in borrow_db.values():
        if b['user_id'] == record.user_id and b['book_id'] == record.book_id and b['status'] == "borrowed":
            raise HTTPException(status_code=409, detail="Conflict")
    
    borrow_id = get_next_borrow_id()
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    borrow_record = {
        "borrow_id": borrow_id,
        "user_id": record.user_id,
        "book_id": record.book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None,
        "status": "borrowed"
    }
    
    borrow_db[borrow_id] = borrow_record
    update_book_copies(record.book_id, -1)
    persist_borrows()
    
    return BorrowReturnModel(**borrow_record)

@app.post("/return", response_model=BorrowReturnModel, status_code=200, description="Return a book")
async def return_book(record: BorrowReturnModel):
    
    for b in borrow_db.values():
        if b['user_id'] == record.user_id and b['book_id'] == record.book_id and b['status'] == "borrowed":
            b['status'] = "returned"
            b['return_date'] = datetime.now().strftime("%Y-%m-%d")
            update_book_copies(b['book_id'], 1)
            persist_borrows()
            return BorrowReturnModel(**b)
    
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/", response_model=list[BorrowReturnModel], status_code=200, description="List all borrow records")
async def list_borrows():
    return [BorrowReturnModel(**b) for b in borrow_db.values()]

@app.get("/user/{user_id}", response_model=list[BorrowReturnModel], status_code=200, description="List borrow records by user")
async def borrows_by_user(user_id: int = Path(..., ge=1)):
    return [BorrowReturnModel(**b) for b in borrow_db.values() if b['user_id'] == user_id]

@app.get("/book/{book_id}", response_model=list[BorrowReturnModel], status_code=200, description="List borrow records by book")
async def borrows_by_book(book_id: int = Path(..., ge=1)):
    return [BorrowReturnModel(**b) for b in borrow_db.values() if b['book_id'] == book_id]

@app.get("/user/{user_id}/book/{book_id}", response_model=BorrowReturnModel, status_code=200, description="Get borrow record by user and book")
async def get_borrow_record(user_id: int = Path(..., ge=1), book_id: int = Path(..., ge=1)):
    for b in borrow_db.values():
        if b['user_id'] == user_id and b['book_id'] == book_id:
            return BorrowReturnModel(**b)
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/check-availability/{book_id}", status_code=200, description="Check if a book is available")
async def check_book_availability(book_id: int = Path(..., ge=1)):
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail="Not Found")
    
    book = book_db[book_id]
    return {
        "book_id": book_id,
        "title": book["title"],
        "available_copies": book["available_copies"],
        "is_available": book["available_copies"] > 0
    }