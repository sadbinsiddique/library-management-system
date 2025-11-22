# file: client/borrow_return.py
import requests

class BorrowReturnClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.base_url = self.base_url.rstrip('/')
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
    
    def borrow_book(self, user_id, book_id):
        return self._request(
            'POST',
            '/borrow',
            json={
                'user_id': user_id,
                'book_id': book_id
            }
        )
    
    def return_book(self, borrow_id):
        return self._request(
            'POST',
            '/return',
            json={
                'borrow_id': borrow_id
            }
        )
    
    def track_user_borrows(self, user_id):
        return self._request(
            'GET',
            f'/track/{user_id}'
        )
    
    def list_borrowed_books(self):
        return self._request(
            'GET',
            '/borrowed-books'
        )

    def check_book_availability(self, book_id):
        return self._request(
            'GET',
            f'/check-availability/{book_id}'
        )
    
def print_borrow(borrow, show_title=True):
    print("\n--- Borrow Record ---")
    print(f"Borrow ID: {borrow.get('borrow_id')}")
    
    if 'user_id' in borrow:
        print(f"User ID: {borrow.get('user_id')}")
    if 'book_id' in borrow:
        print(f"Book ID: {borrow.get('book_id')}")
    if show_title and 'book_title' in borrow:
        print(f"Book Title: {borrow.get('book_title')}")
    if 'author' in borrow:
        print(f"Author: {borrow.get('author')}")
    
    print(f"Borrow Date: {borrow.get('borrow_date')}")
    print(f"Due Date: {borrow.get('due_date')}")
    
    if borrow.get('return_date'):
        print(f"Return Date: {borrow.get('return_date')}")
    print(f"Status: {borrow.get('status')}")
    
    print()

def print_availability(availability):
    print("\n--- Book Availability ---")
    print(f"Book ID: {availability.get('book_id')}")
    print(f"Book Title: {availability.get('book_title')}")
    print(f"Author: {availability.get('author')}")
    print(f"Copies Available: {availability.get('total_copies')}")
    print(f"Status: {availability.get('status')}")
    print()