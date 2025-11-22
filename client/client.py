# file: client/client.py
import os
import sys
from book_management import BookManagementClient, print_book
from user_management import UserManagementClient, print_user

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt(msg, type_func=str):
    while True:
        try:
            val = input(msg).strip()
            return type_func(val) if val else None
        except (ValueError, KeyboardInterrupt):
            print("Invalid input.")

def book_management_menu():
    client = BookManagementClient("http://127.0.0.1:8000/book")
    
    while True:
        clear_screen()
        print("\n╔════════════════════════════════════╗")
        print("║  Book Management                   ║")
        print("╚════════════════════════════════════╝")
        print("1. Add Book")
        print("2. List Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("b. Back to Main Menu\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'b':
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

def user_management_menu():
    client = UserManagementClient("http://127.0.0.1:8000/user")
    
    while True:
        clear_screen()
        print("\n╔════════════════════════════════════╗")
        print("║  User Management                   ║")
        print("╚════════════════════════════════════╝")
        print("1. Add User")
        print("2. List Users")
        print("3. Search User")
        print("4. Update User")
        print("5. Delete User")
        print("b. Back\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'b':
            break
            
        try:
            if cmd == '1':
                user = client.add_user(
                    input("Username: "), 
                    input("Full Name: "), 
                    input("Email: ")
                )
                print_user(user)
                
            elif cmd == '2':
                data = client.list_users()
                users = data.get('users', data) if isinstance(data, dict) else data
                if isinstance(users, dict):
                    for uid, u in sorted(users.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0]):
                        print_user(u, uid)
                else:
                    for u in users:
                        print_user(u, u.get('id'))
                        
            elif cmd == '3':
                user = client.get_user(input("User ID: "))
                print_user(user)
                
            elif cmd == '4':
                user_id = input("User ID: ")
                updated = client.update_user(
                    user_id,
                    username=prompt("Username: "),
                    full_name=prompt("Full Name: "),
                    email=prompt("Email: ")
                )
                print_user(updated, user_id)
                
            elif cmd == '5':
                client.delete_user(input("User ID: "))
                print("Deleted successfully!")
                
            input("\nPress Enter to continue... ")
        except Exception as e:
            print(f"{e}")
            input("\nPress Enter to continue... ")

def main_menu():
    """Main Menu - Switch between management modules"""
    while True:
        clear_screen()
        print("\n╔════════════════════════════════════╗")
        print("║  Library Management System Client  ║")
        print("╚════════════════════════════════════╝")
        print("\n1. Book Management")
        print("2. User Management")
        print("q. Quit\n")
        
        choice = input("Select Module: ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            sys.exit(0)
        elif choice == '1':
            book_management_menu()
        elif choice == '2':
            user_management_menu()
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue... ")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
