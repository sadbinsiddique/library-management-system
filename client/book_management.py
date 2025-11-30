import requests

class BookManagementClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
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

    def add_book(self, title, author, isbn, published_year, available_copies):
        return self._request('POST', '/', json={'title': title, 'author': author, 'isbn': isbn, 'published_year': published_year, 'available_copies': available_copies})

    def get_book(self, book_id):
        return self._request('GET', f'/{book_id}')

    def update_book(self, book_id, **fields):
        update_data = {k: v for k, v in fields.items() if v is not None}
        return self._request('PUT', f'/{book_id}', json=update_data)

    def delete_book(self, book_id):
        self._request('DELETE', f'/{book_id}')

    def list_books(self):
        return self._request( 'GET', '/')

def print_book(book, book_id=None):
    print(f"ID: {book_id} Title: {book.get('title')} Author: {book.get('author')} ISBN: {book.get('isbn')} Published Year: {book.get('published_year')} Available Copies: {book.get('available_copies')}")
    
    
        
    