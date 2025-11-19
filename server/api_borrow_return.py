from fastapi import FastAPI, Query, Path, HTTPException
from .api_book_management import book_db
from .api_user_management import user_db
from pydantic import BaseModel
from typing import List


app = FastAPI(title="Borrow & Return System")

borrow_book_db = []

class BorrowReturnModel(BaseModel):
    user_id: int
    book_id: int
    date: str # YYYY-MM-DD format

@app.post("/", response_model=BorrowReturnModel, status_code=201)
async def borrow_book(record: BorrowReturnModel):
    # Validate user exists
    if record.user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate book exists
    if record.book_id not in book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if already borrowed
    for existing in borrow_book_db:
        if existing.user_id == record.user_id and existing.book_id == record.book_id:
            raise HTTPException(status_code=409, detail="Book already borrowed by user")
    
    if book_db[record.book_id].get("copies_available", 0) < 1:
        raise HTTPException(status_code=400, detail="Not enough copies available")
    
    book_db[record.book_id]["copies_available"] -= 1
    borrow_book_db.append(record)
    return record

@app.delete("/return", response_model=BorrowReturnModel, status_code=200)
async def return_book(record: BorrowReturnModel):
    # Validate book exists
    if record.book_id not in book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for existing in borrow_book_db:
        if existing.user_id == record.user_id and existing.book_id == record.book_id:
            book_db[record.book_id]["copies_available"] += 1
            borrow_book_db.remove(existing)
            return record
    
    raise HTTPException(status_code=404, detail="Borrow record not found")

@app.get("/", response_model=List[BorrowReturnModel])
async def list_borrows():
    return borrow_book_db

@app.get("/user/{user_id}", response_model=List[BorrowReturnModel])
async def borrows_by_user(user_id: int = Path(..., ge=1)):
    return [r for r in borrow_book_db if r.user_id == user_id]

@app.get("/book/{book_id}", response_model=List[BorrowReturnModel])
async def borrows_by_book(book_id: int = Path(..., ge=1)):
    return [r for r in borrow_book_db if r.book_id == book_id]

@app.get("/user/{user_id}/book/{book_id}", response_model=BorrowReturnModel)
async def get_borrow_record(user_id: int = Path(..., ge=1), book_id: int = Path(..., ge=1)):
    for r in borrow_book_db:
        if r.user_id == user_id and r.book_id == book_id:
            return r
    raise HTTPException(status_code=404, detail="Borrow record not found")