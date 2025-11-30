import requests

class BorrowReturnClient:
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

    def borrow_book(self, user_id, book_id):
        return self._request('POST', '/', json={'user_id': user_id, 'book_id': book_id})

    def return_book(self, user_id, book_id):
        return self._request('POST', '/return', json={'user_id': user_id, 'book_id': book_id})

    def list_borrows(self):
        return self._request('GET', '/')

    def track_user_borrows(self, user_id):
        return self._request('GET', f'/user/{user_id}')

    def borrows_by_book(self, book_id):
        return self._request('GET', f'/book/{book_id}')

    def get_borrow_record(self, user_id, book_id):
        return self._request('GET', f'/user/{user_id}/book/{book_id}')
    
    def check_book_availability(self, book_id):
        return self._request('GET', f'/check-availability/{book_id}')

def print_borrow(borrow):
    print(f"Borrow ID: {borrow.get('borrow_id')} User ID: {borrow.get('user_id')} Book ID: {borrow.get('book_id')} Borrow Date: {borrow.get('borrow_date')} Due Date: {borrow.get('due_date')} Return Date: {borrow.get('return_date')} Status: {borrow.get('status')}\n")