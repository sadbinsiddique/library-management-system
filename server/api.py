from fastapi import FastAPI
from .api_book_management import app as book_management # relative import

app = FastAPI(
    title="Library Management System",
    description="A comprehensive API service for Library Management System with Book Management, User Management, Borrow & Return System and Reports features.",
    version="2.1.0",
)

app.mount("/book", book_management)

@app.get("/", response_model=dict, status_code=200)
async def root():
    return {"title": app.title, "version": app.version, "description": app.description}