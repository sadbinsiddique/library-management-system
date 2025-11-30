from fastapi import FastAPI, HTTPException
from helpers.read_db import load_books, load_users, load_borrows
from datetime import datetime
from typing import Optional

app = FastAPI()

def get_all_books_data():
    books = load_books()
    return books

def get_all_users_data():
    users = load_users()
    return users

def get_all_borrows_data():
    borrows = load_borrows()
    return borrows

def get_overdue_books():
    borrows = load_borrows()
    books = load_books()
    users = load_users()
    
    books_dict = {book["id"]: book for book in books}
    users_dict = {user["id"]: user for user in users}
    
    overdue_list = []
    today = datetime.now().date()
    
    for borrow in borrows:
        if borrow["status"] == "borrowed":
            due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d").date()
            if due_date < today:
                days_overdue = (today - due_date).days
                book = books_dict.get(borrow["book_id"], {})
                user = users_dict.get(borrow["user_id"], {})
                
                overdue_list.append({
                    "borrow_id": borrow["borrow_id"],
                    "user_id": borrow["user_id"],
                    "username": user.get("username", "Unknown"),
                    "book_id": borrow["book_id"],
                    "book_title": book.get("title", "Unknown"),
                    "borrow_date": borrow["borrow_date"],
                    "due_date": borrow["due_date"],
                    "days_overdue": days_overdue
                })
    
    return overdue_list

def get_most_borrowed_books():
    borrows = load_borrows()
    books = load_books()
    
    books_dict = {book["id"]: book for book in books}
    
    borrow_count = {}
    for borrow in borrows:
        book_id = borrow["book_id"]
        borrow_count[book_id] = borrow_count.get(book_id, 0) + 1
    
    sorted_books = sorted(borrow_count.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    for book_id, count in sorted_books[:10]: 
        book = books_dict.get(book_id, {})
        result.append({
            "book_id": book_id,
            "title": book.get("title", "Unknown"),
            "author": book.get("author", "Unknown"),
            "times_borrowed": count
        })
    
    return result

def get_borrowing_history(user_id: Optional[int] = None):
    borrows = load_borrows()
    books = load_books()
    users = load_users()
    
    books_dict = {book["id"]: book for book in books}
    users_dict = {user["id"]: user for user in users}
    
    history = []
    for borrow in borrows:
        if user_id is None or borrow["user_id"] == user_id:
            book = books_dict.get(borrow["book_id"], {})
            user = users_dict.get(borrow["user_id"], {})
            
            history.append({
                "borrow_id": borrow["borrow_id"],
                "user_id": borrow["user_id"],
                "username": user.get("username", "Unknown"),
                "book_id": borrow["book_id"],
                "book_title": book.get("title", "Unknown"),
                "borrow_date": borrow["borrow_date"],
                "due_date": borrow["due_date"],
                "return_date": borrow.get("return_date"),
                "status": borrow["status"]
            })
    
    return history

@app.get("/reports", response_model=dict, status_code=200)
async def get_all_reports():
    """Get comprehensive admin report with all system data"""
    try:
        books_data = get_all_books_data()
        users_data = get_all_users_data()
        borrows_list = get_all_borrows_data()
        
        active_borrows = sum(1 for b in borrows_list if b['status'] == 'borrowed')
        returned_borrows = sum(1 for b in borrows_list if b['status'] == 'returned')
        total_copies = sum(book["available_copies"] for book in books_data)
        
        return {
            "summary": {
                "total_books": len(books_data),
                "total_users": len(users_data),
                "total_borrows": len(borrows_list),
                "active_borrows": active_borrows,
                "returned_borrows": returned_borrows,
                "total_copies_available": total_copies
            },
            "books": books_data,
            "users": users_data,
            "borrows": borrows_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/reports/overdue", response_model=list, status_code=200)
async def get_overdue_report():
    try:
        return get_overdue_books()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching overdue books: {str(e)}")

@app.get("/reports/most-borrowed", response_model=list, status_code=200)
async def get_most_borrowed_report():
    try:
        return get_most_borrowed_books()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching most borrowed books: {str(e)}")

@app.get("/reports/history", response_model=list, status_code=200)
async def get_borrowing_history_report(user_id: Optional[int] = None):
    try:
        return get_borrowing_history(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching borrowing history: {str(e)}")
