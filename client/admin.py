# file: client/admin.py
import requests

class AdminClient:
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

    def get_all_reports(self):
        """Get comprehensive report with books, users, and borrows information"""
        return self._request('GET', '/reports')

def print_summary(summary):
    """Print the summary statistics"""
    print("\n" + "="*50)
    print("LIBRARY MANAGEMENT SYSTEM - SUMMARY REPORT")
    print("="*50)
    print(f"Total Books: {summary.get('total_books')}")
    print(f"Total Users: {summary.get('total_users')}")
    print(f"Total Borrows: {summary.get('total_borrows')}")
    print(f"Active Borrows: {summary.get('active_borrows')}")
    print(f"Returned Borrows: {summary.get('returned_borrows')}")
    print("="*50 + "\n")

def print_books_report(books):
    """Print detailed books information"""
    print("\n" + "-"*50)
    print("BOOKS REPORT")
    print("-"*50)
    
    if not books:
        print("No books found in the system.\n")
        return
    
    for book in books:
        print(f"\nBook ID: {book.get('id')}")
        print(f"  Title: {book.get('title')}")
        print(f"  Author: {book.get('author')}")
        print(f"  ISBN: {book.get('isbn')}")
        print(f"  Published Year: {book.get('published_year')}")
        print(f"  Available Copies: {book.get('available_copies')}")
        print("-" * 30)
    print()

def print_users_report(users):
    """Print detailed users information"""
    print("\n" + "-"*50)
    print("USERS REPORT")
    print("-"*50)
    
    if not users:
        print("No users found in the system.\n")
        return
    
    for user in users:
        print(f"\nUser ID: {user.get('id')}")
        print(f"  Username: {user.get('username')}")
        print(f"  Full Name: {user.get('full_name')}")
        print(f"  Email: {user.get('email')}")
        print("-" * 30)
    print()

def print_borrows_report(borrows):
    """Print detailed borrows information"""
    print("\n" + "-"*50)
    print("BORROWS REPORT")
    print("-"*50)
    
    if not borrows:
        print("No borrow records found in the system.\n")
        return
    
    for borrow in borrows:
        print(f"\nBorrow ID: {borrow.get('borrow_id')}")
        print(f"  User ID: {borrow.get('user_id')}")
        print(f"  Book ID: {borrow.get('book_id')}")
        print(f"  Borrow Date: {borrow.get('borrow_date')}")
        print(f"  Due Date: {borrow.get('due_date')}")
        print(f"  Return Date: {borrow.get('return_date') if borrow.get('return_date') else 'Not returned yet'}")
        print(f"  Status: {borrow.get('status')}")
        print("-" * 30)
    print()

def print_full_report(report_data):
    """Print complete report with all sections"""
    # Print summary
    if 'summary' in report_data:
        print_summary(report_data['summary'])
    
    # Print books report
    if 'books' in report_data:
        print_books_report(report_data['books'])
    
    # Print users report
    if 'users' in report_data:
        print_users_report(report_data['users'])
    
    # Print borrows report
    if 'borrows' in report_data:
        print_borrows_report(report_data['borrows'])

