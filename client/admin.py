import requests

class AdminClient:
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
    
    def get_all_reports(self):
        return self._request('GET', '/reports')
    
    def get_overdue_books(self):
        return self._request('GET', '/reports/overdue')
    
    def get_most_borrowed_books(self):
        return self._request('GET', '/reports/most-borrowed')
    
    def get_borrowing_history(self, user_id=None):
        params = {'user_id': user_id} if user_id else {}
        return self._request('GET', '/reports/history', params=params)

def print_summary(summary):
    print("LIBRARY MANAGEMENT SYSTEM - SUMMARY REPORT".center(60))
    print(f"Total Books: {summary.get('total_books')}")
    print(f"Total Users: {summary.get('total_users')}")
    print(f"Total Borrows: {summary.get('total_borrows')}")
    print(f"Active Borrows: {summary.get('active_borrows')}")
    print(f"Returned Borrows: {summary.get('returned_borrows')}")
    print(f"Total Copies Available: {summary.get('total_copies_available', 'N/A')}")

def print_books_report(books):
    print("BOOKS REPORT".center(60))
    if not books:
        print("No books found in the system.")
        return
    
    for book in books:
        print(f"Book ID: {book.get('id')} Title: {book.get('title')} Author: {book.get('author')} ISBN: {book.get('isbn')} Published Year: {book.get('published_year')} Available Copies: {book.get('available_copies')}")
        

def print_users_report(users):
    print("USERS REPORT".center(60))
    if not users:
        print("No users found in the system.")
        return
    
    for user in users:
        print(f"User ID: {user.get('id')} Username: {user.get('username')} Full Name: {user.get('full_name')} Email: {user.get('email')}")

def print_borrows_report(borrows):
    print("BORROWS REPORT".center(60))
    if not borrows:
        print("No borrow records found in the system.")
        return
    
    for borrow in borrows:
        print(f"Borrow ID: {borrow.get('borrow_id')} User ID: {borrow.get('user_id')} Book ID: {borrow.get('book_id')} Borrow Date: {borrow.get('borrow_date')} Due Date: {borrow.get('due_date')} Return Date: {borrow.get('return_date') or 'Not returned yet'} Status: {borrow.get('status')}")

def print_overdue_report(overdue_books):
    print("OVERDUE BOOKS REPORT".center(60))
    if not overdue_books:
        print("No overdue books found.")
        return
    
    for item in overdue_books:
        print(f"Borrow ID: {item.get('borrow_id')} User: {item.get('username')} (ID: {item.get('user_id')}) Book: {item.get('book_title')} (ID: {item.get('book_id')}) Due Date: {item.get('due_date')} Days Overdue: {item.get('days_overdue')}")

def print_most_borrowed_report(most_borrowed):
    print("MOST BORROWED BOOKS REPORT".center(60))
    if not most_borrowed:
        print("No borrowing data available.")
        return
    
    for idx, item in enumerate(most_borrowed, 1):
        print(f"{idx}. {item.get('title')} Author: {item.get('author')} Book ID: {item.get('book_id')} Times Borrowed: {item.get('times_borrowed')}")

def print_borrowing_history(history):
    print("BORROWING HISTORY REPORT".center(60))
    if not history:
        print("No borrowing history available.")
        return
    
    for item in history:
        print(f"Borrow ID: {item.get('borrow_id')} User: {item.get('username')} (ID: {item.get('user_id')}) Book: {item.get('book_title')} (ID: {item.get('book_id')}) Borrow Date: {item.get('borrow_date')} Due Date: {item.get('due_date')} Return Date: {item.get('return_date') or 'Not returned yet'} Status: {item.get('status')}")

def print_full_report(report_data):
    if 'summary' in report_data:
        print_summary(report_data['summary'])
    
    if 'books' in report_data:
        print_books_report(report_data['books'])
    
    if 'users' in report_data:
        print_users_report(report_data['users'])
    
    if 'borrows' in report_data:
        print_borrows_report(report_data['borrows'])
