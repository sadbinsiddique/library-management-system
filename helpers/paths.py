import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
BOOKS_FILE = os.path.join(DATABASE_DIR, "books.txt")
USERS_FILE = os.path.join(DATABASE_DIR, "users.txt")
BORROWS_FILE = os.path.join(DATABASE_DIR, "borrows.txt")