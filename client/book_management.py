# file: client/book_management.py
import requests

class BookManagementClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        kwargs.setdefault('timeout', self.timeout)

        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
            return None if resp.status_code == 204 else resp.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def add_book(self, title, author, isbn, published_year, copies_available):
        return self._request(
            'POST', 
            '', 
            json={
                'title': title, 
                'author': author, 
                'isbn': isbn,
                'published_year': published_year, 
                'copies_available': copies_available
        })

    def get_book(self, book_id):
        return self._request(
            'GET', 
            f'/{book_id}'
        )

    def update_book(self, book_id, **fields):
        update_data = {k: v for k, v in fields.items() if v is not None}
        return self._request(
            'PUT', 
            f'/{book_id}',
            json=update_data
        )

    def delete_book(self, book_id):
        self._request(
            'DELETE', 
            f'/{book_id}'
        )

    def list_books(self):
        return self._request(
            'GET', 
            ''
        )

def print_book(book, book_id=None):
    print("\n--- Book Info ---")
    if book_id: 
        print(f"ID: {book_id}")

    print(f"Title: {book.get('title')}")
    print(f"Author: {book.get('author')}")
    print(f"ISBN: {book.get('isbn')}")
    print(f"Year: {book.get('published_year')}")
    print(f"Copies: {book.get('copies_available')}\n")