# **Library Management System**

An API service to demonstrate Library Management System API capabilities.

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
| Book Management | Add  book | Update book | Delete book | Show all books | Search book by title/author |
| Member Management | Add  member | Update member | Delete member | Show all members | Search member by name |
| Borrow & Return System | Borrow book | Return book | Track which member borrowed which book | List all borrowed books | Check if a book is available |
| Reports & Admin | Overdue books | Most borrowed book | Borrowing history | Generate member receipt (file-based) | Admin login authentication |

> Note : Hare Eatch `Feature Name` consider as API Services &  `Feature [1-5]` consider as console Server

## Services

### API

```bash
uvicorn api_server:app --reload
```

### Console

```bash
python api_client.py
```
