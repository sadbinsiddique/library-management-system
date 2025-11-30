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
    print("\n" + "="*60)
    print("LIBRARY MANAGEMENT SYSTEM - SUMMARY REPORT".center(60))
    print("="*60)
    print(f"Total Books: {summary.get('total_books')}")
    print(f"Total Users: {summary.get('total_users')}")
    print(f"Total Borrows: {summary.get('total_borrows')}")
    print(f"Active Borrows: {summary.get('active_borrows')}")
    print(f"Returned Borrows: {summary.get('returned_borrows')}")
    print(f"Total Copies Available: {summary.get('total_copies_available', 'N/A')}")
    print("="*60 + "\n")

def print_books_report(books):
    print("\n" + "-"*60)
    print("BOOKS REPORT".center(60))
    print("-"*60)
    if not books:
        print("No books found in the system.\n")
        return
    
    for book in books:
        print(f"\nBook ID: {book.get('id')}")
        print(f"  Title: {book.get('title')}")
        print(f"  Author: {book.get('author')}")
        print(f"  ISBN: {book.get('isbn')}")
        print(f"  Published Year: {book.get('published_year')}")
        print(f"  Available Copies: {book.get('copies_available')}")
        print("-" * 40)
    print()

def print_users_report(users):
    print("\n" + "-"*60)
    print("USERS REPORT".center(60))
    print("-"*60)
    if not users:
        print("No users found in the system.\n")
        return
    
    for user in users:
        print(f"\nUser ID: {user.get('id')}")
        print(f"  Username: {user.get('username')}")
        print(f"  Full Name: {user.get('full_name')}")
        print(f"  Email: {user.get('email')}")
        print("-" * 40)
    print()

def print_borrows_report(borrows):
    print("\n" + "-"*60)
    print("BORROWS REPORT".center(60))
    print("-"*60)
    if not borrows:
        print("No borrow records found in the system.\n")
        return
    
    for borrow in borrows:
        print(f"\nBorrow ID: {borrow.get('borrow_id')}")
        print(f"  User ID: {borrow.get('user_id')}")
        print(f"  Book ID: {borrow.get('book_id')}")
        print(f"  Borrow Date: {borrow.get('borrow_date')}")
        print(f"  Due Date: {borrow.get('due_date')}")
        print(f"  Return Date: {borrow.get('return_date') or 'Not returned yet'}")
        print(f"  Status: {borrow.get('status')}")
        print("-" * 40)
    print()

def print_overdue_report(overdue_books):
    print("\n" + "-"*60)
    print("OVERDUE BOOKS REPORT".center(60))
    print("-"*60)
    if not overdue_books:
        print("No overdue books found.\n")
        return
    
    for item in overdue_books:
        print(f"\nBorrow ID: {item.get('borrow_id')}")
        print(f"  User: {item.get('username')} (ID: {item.get('user_id')})")
        print(f"  Book: {item.get('book_title')} (ID: {item.get('book_id')})")
        print(f"  Due Date: {item.get('due_date')}")
        print(f"  Days Overdue: {item.get('days_overdue')}")
        print("-" * 40)
    print()

def print_most_borrowed_report(most_borrowed):
    print("\n" + "-"*60)
    print("MOST BORROWED BOOKS REPORT".center(60))
    print("-"*60)
    if not most_borrowed:
        print("No borrowing data available.\n")
        return
    
    for idx, item in enumerate(most_borrowed, 1):
        print(f"\n{idx}. {item.get('title')}")
        print(f"   Author: {item.get('author')}")
        print(f"   Book ID: {item.get('book_id')}")
        print(f"   Times Borrowed: {item.get('times_borrowed')}")
        print("-" * 40)
    print()

def print_borrowing_history(history):
    print("\n" + "-"*60)
    print("BORROWING HISTORY REPORT".center(60))
    print("-"*60)
    if not history:
        print("No borrowing history available.\n")
        return
    
    for item in history:
        print(f"\nBorrow ID: {item.get('borrow_id')}")
        print(f"  User: {item.get('username')} (ID: {item.get('user_id')})")
        print(f"  Book: {item.get('book_title')} (ID: {item.get('book_id')})")
        print(f"  Borrow Date: {item.get('borrow_date')}")
        print(f"  Due Date: {item.get('due_date')}")
        print(f"  Return Date: {item.get('return_date') or 'Not returned yet'}")
        print(f"  Status: {item.get('status')}")
        print("-" * 40)
    print()

def print_full_report(report_data):
    if 'summary' in report_data:
        print_summary(report_data['summary'])
    
    if 'books' in report_data:
        print_books_report(report_data['books'])
    
    if 'users' in report_data:
        print_users_report(report_data['users'])
    
    if 'borrows' in report_data:
        print_borrows_report(report_data['borrows'])
