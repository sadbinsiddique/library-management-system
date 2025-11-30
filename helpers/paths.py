import os
import sys
import shutil

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    app_root = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
        "library-management-system",
    )
    DATABASE_DIR = os.path.join(app_root, "database")

    os.makedirs(DATABASE_DIR, exist_ok=True)

    bundled_db_dir = os.path.join(getattr(sys, "_MEIPASS"), "database")
    for fname in ("books.txt", "users.txt", "borrows.txt"):
        src = os.path.join(bundled_db_dir, fname)
        dst = os.path.join(DATABASE_DIR, fname)
        if not os.path.exists(dst) and os.path.exists(src):
            shutil.copy2(src, dst)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_DIR = os.path.join(BASE_DIR, "database")

BOOKS_FILE = os.path.join(DATABASE_DIR, "books.txt")
USERS_FILE = os.path.join(DATABASE_DIR, "users.txt")
BORROWS_FILE = os.path.join(DATABASE_DIR, "borrows.txt")
