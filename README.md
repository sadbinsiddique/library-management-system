# **Library Management System**

A comprehensive API service for Library Management System with Book Management, User Management, Borrow & Return System and Reports features.

## Required Libraries

- [`Python`](https://docs.python.org/3/)
- [`Fastapi`](https://fastapi.tiangolo.com)
- [`Requests`](https://www.w3schools.com/python/module_requests.asp)
- [`uvicorn`](https://uvicorn.dev)

## Entity

- User
- Book
- Borrow

## API Feature

|  Name | Feature 1 | Feature 2 | Feature 3 | Feature 4 | Feature 5 |
| --- | --- | --- | --- | --- | --- |
| [Book Management](http://127.0.0.1:8000/book/docs) | Add  book | Update book | Delete book | List Books | Search book by Id |
| [User Management](http://127.0.0.1:8000/user/docs) | Add  User | Update User | Delete User | List Users | Search User by Id |
| [Borrow & Return System](http://127.0.0.1:8000/borrow/docs) | Borrow book | Return book | Track Users Borrowed Books | List all borrowed books | Check book availability |
| [Reports & Admin](http://127.0.0.1:8000/admin/docs) | View Complete System Report | View Summary Statistics | View Overdue Books | View Most Borrowed Books | View User-Specific Borrowing History |

## Services

### 1. Virtual Environment

Create the virtual environment:

```cmd
python -m venv .venv
```

Activate

```cmd
.venv\Scripts\activate
```

### 2. Install the dependencies

```cmd
pip install -r requirements.txt
```

### 3. Server

```cmd
python main.py
```

### 4. Client

```cmd
python client/client.py
```

### 5. Build Single EXE (Windows)

Build a one-file Windows executable with PyInstaller.

Prerequisites:

- Python on PATH
- Dependencies installed: `pip install -r requirements.txt`

Quick build (cmd.exe):

```cmd
build.bat
```

This creates `dist\library-management-system.exe`.

Manual command if preferred:

```cmd
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --name library-management-system --add-data "database;database" main.py
```

Notes:

- Data files from `database/` are bundled and discovered at runtime (handled in `helpers/paths.py`).
- Uvicorn reload is disabled inside the EXE to avoid watcher/spawn issues.
- When running as an EXE, data is stored under `%LOCALAPPDATA%\library-management-system\database` so changes persist across runs.
