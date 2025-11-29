# **Library Management System**

A comprehensive API service for Library Management System with Book Management, User Management, Borrow & Return System and Reports features.

## Required Libraries

- [`Python`](https://docs.python.org/3/)
- [`Fastapi`](https://fastapi.tiangolo.com)
- [`Requests`](https://www.w3schools.com/python/module_requests.asp)
- [`uvicorn`](https://uvicorn.dev)

## Entity

- Book
- Member

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

```bash
# Use `python` or `python3` as appropriate
python -m venv .venv
```=kv

Activate

- Windows (cmd.exe)
```cmd
.venv\Scripts\activate
```

- Linux / macOS / WSL / Git Bash

```bash
source .venv/bin/activate
```

Deactivate

```bash
deactivate
```

### 2. Server

```bash
python main.py
```

### 3. Client

```bash
cd client
python client.py
```

## Project Tree

```bash
library-management-system
│    │
│    ├──server
│    │    ├───api_book_management
│    │    ├───api_user_management
│    │    ├───api_borrow_return_system
│    │    ├───api_admin
│    │    └───app
│    │
│    └───client
│         ├───book_management
│         ├───user_management
│         ├───borrow_return_system
│         ├───admin
│         └───client
│    
└───main
```
