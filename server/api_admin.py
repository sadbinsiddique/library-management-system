# file: server/api_admin.py
from fastapi import FastAPI
import os

app = FastAPI()

# File paths
BOOKS_FILE = 'database/books.txt'
USERS_FILE = 'database/users.txt'
BORROWS_FILE = 'database/borrows.txt'

def ensure_database_directory():
    """Ensure database directory and files exist"""
    os.makedirs("database", exist_ok=True)
    for file in [BOOKS_FILE, USERS_FILE, BORROWS_FILE]:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass

def get_all_books_data():
    """Get all books from book management system"""
    ensure_database_directory()
    books = {}
    
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    book_id = parts[0]
                    books[book_id] = {
                        "id": book_id,
                        "title": parts[1],
                        "author": parts[2],
                        "isbn": parts[3],
                        "published_year": int(parts[4]),
                        "copies_available": int(parts[5])
                    }
    return books

def get_all_users_data():
    """Get all users from user management system"""
    ensure_database_directory()
    users = {}
    
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    user_id = parts[0]
                    users[user_id] = {
                        "id": user_id,
                        "username": parts[1],
                        "full_name": parts[2],
                        "email": parts[3]
                    }
    return users

def get_all_borrows_data():
    """Get all borrow records from borrow/return system"""
    ensure_database_directory()
    borrows = []
    
    if os.path.exists(BORROWS_FILE):
        with open(BORROWS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    borrows.append({
                        "borrow_id": int(parts[0]),
                        "user_id": int(parts[1]),
                        "book_id": int(parts[2]),
                        "borrow_date": parts[3],
                        "due_date": parts[4],
                        "return_date": parts[5] if parts[5] else None,
                        "status": parts[6]
                    })
    return borrows

@app.get("/reports", response_model=dict, status_code=200)
async def get_all_reports():
    """Get comprehensive admin report with all system data"""
    ensure_database_directory()
    
    # Get data from all modules
    books_dict = get_all_books_data()
    users_dict = get_all_users_data()
    borrows_list = get_all_borrows_data()
    
    # Convert to list format for easier display
    books_data = list(books_dict.values())
    users_data = list(users_dict.values())
    
    # Calculate statistics
    active_borrows = sum(1 for b in borrows_list if b['status'] == 'borrowed')
    returned_borrows = sum(1 for b in borrows_list if b['status'] == 'returned')
    
    return {
        "summary": {
            "total_books": len(books_data),
            "total_users": len(users_data),
            "total_borrows": len(borrows_list),
            "active_borrows": active_borrows,
            "returned_borrows": returned_borrows
        },
        "books": books_data,
        "users": users_data,
        "borrows": borrows_list
    }
