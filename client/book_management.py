import requests
import os

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
        return self._request('POST', '/', json={
            'title': title, 'author': author, 'isbn': isbn,
            'published_year': published_year, 'copies_available': copies_available
        })

    def get_book(self, book_id):
        return self._request('GET', f'/{book_id}')

    def update_book(self, book_id, **fields):
        return self._request('PUT', f'/{book_id}', json={k: v for k, v in fields.items() if v})

    def delete_book(self, book_id):
        self._request('DELETE', f'/{book_id}')

    def list_books(self):
        return self._request('GET', '/')

def prompt(msg, type_func=str):
    while True:
        try:
            val = input(msg).strip()
            return type_func(val) if val else None
        except (ValueError, KeyboardInterrupt):
            print("Invalid input. Try again.")

def print_book(book, book_id=None):
    print("\n--- Book Info ---")
    if book_id: print(f"ID: {book_id}")
    print(f"Title: {book.get('title')}")
    print(f"Author: {book.get('author')}")
    print(f"ISBN: {book.get('isbn')}")
    print(f"Year: {book.get('published_year')}")
    print(f"Copies: {book.get('copies_available')}\n")

if __name__ == "__main__":
    client = BookManagementClient("http://127.0.0.1:8000/book")
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n====== Book Management ======")
        print("1. Add Book")
        print("2. List Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("q. Quit\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'q':
            break
            
        try:
            if cmd == '1':
                book = client.add_book(
                    input("Title: "), 
                    input("Author: "), 
                    input("ISBN: "),
                    int(input("Year: ")), 
                    int(input("Copies: "))
                )
                print_book(book)
                
            elif cmd == '2':
                data = client.list_books()
                books = data.get('books', data) if isinstance(data, dict) else data
                if isinstance(books, dict):
                    for bid, b in sorted(books.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0]):
                        print_book(b, bid)
                else:
                    for b in books:
                        print_book(b, b.get('id'))
                        
            elif cmd == '3':
                book = client.get_book(input("Book ID: "))
                print_book(book)
                
            elif cmd == '4':
                book_id = input("Book ID: ")
                updated = client.update_book(
                    book_id,
                    title=prompt("Title: "),
                    author=prompt("Author: "),
                    isbn=prompt("ISBN: "),
                    published_year=prompt("Year: ", int),
                    copies_available=prompt("Copies: ", int)
                )
                print_book(updated, book_id)
                
            elif cmd == '5':
                client.delete_book(input("Book ID: "))
                print("Deleted successfully!")
                
            input("\nPress Enter to continue... ")
        except Exception as e:
            print(f"{e}")
            input("\nPress Enter to continue... ")
