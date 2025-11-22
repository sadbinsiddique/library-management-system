# file: client/client.py
import os
import sys
from book_management import BookManagementClient, print_book
from user_management import UserManagementClient, print_user
from borrow_return import BorrowReturnClient, print_borrow, print_availability

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
        print("4. Update Book Info")
        print("5. Delete Book")
        print("b. Back to Main Menu\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'b':
            break
            
        try:
            if cmd == '1':
                try:
                    title = input("Title: ").strip()
                    author = input("Author: ").strip()
                    isbn = input("ISBN: ").strip()
                    year = int(input("Year: "))
                    copies = int(input("Copies: "))
                    
                    if not title or not author or not isbn:
                        print("\nError: Title, Author, and ISBN cannot be empty!")
                        continue
                    
                    if year < 1000 or year > 2100:
                        print("\nError: Please enter a valid year (1000-2100)!")
                        continue
                    
                    if copies < 0:
                        print("\nError: Number of copies cannot be negative!")
                        continue
                    
                    book = client.add_book(title, author, isbn, year, copies)
                    print("\n------- Book Added Successfully! ------ \n")
                    print_book(book)
                    
                except ValueError:
                    print("\nError: Year and Copies must be valid numbers!")
                except Exception as e:
                    error_msg = str(e)
                    if "409" in error_msg:
                        print("\nError: A book with this ISBN already exists!")
                    else:
                        print(f"\nError: Failed to add book.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '2':
                try:
                    data = client.list_books()
                    books = data.get('books', data) if isinstance(data, dict) else data
                    
                    if not books or (isinstance(books, dict) and len(books) == 0):
                        print("\nNo books found in the library!")
                    else:
                        print("\n--- All Books ---")
                        if isinstance(books, dict):
                            for bid, b in sorted(books.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0]):
                                print_book(b, bid)
                        else:
                            for b in books:
                                print_book(b, b.get('id'))
                                
                except Exception as e:
                    print(f"\nError: Failed to retrieve books list.")
                    print(f"Details: {e}")
                        
            elif cmd == '3':
                try:
                    book_id = input("Book ID: ").strip()
                    
                    if not book_id:
                        print("\nError: Book ID cannot be empty!")
                        continue
                    
                    book = client.get_book(book_id)
                    print("\n------- Book Found! -------\n")
                    print_book(book)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print(f"\nError: Failed to search for book.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '4':
                try:
                    book_id = input("Book ID: ").strip()
                    
                    if not book_id:
                        print("\nError: Book ID cannot be empty!")
                        continue

                    try:
                        existing_book = client.get_book(book_id)
                        print("\n--- Current Book Details ---")
                        print_book(existing_book, book_id)
                    except Exception as e:
                        if "404" in str(e):
                            print(f"\nError: Book with ID '{book_id}' does not exist!")
                            print("Please check the Book ID and try again.")
                        else:
                            print(f"\nError: Unable to retrieve book details.")
                            print(f"Details: {e}")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    print("\nLeave fields blank to keep current values:")
                    title = prompt("Title: ")
                    author = prompt("Author: ")
                    isbn = prompt("ISBN: ")
                    published_year = prompt("Year: ", int)
                    copies_available = prompt("Copies: ", int)
                    
                    if published_year is not None and (published_year < 1000 or published_year > 2100):
                        print("\nError: Please enter a valid year (1000-2100)!")
                        continue
                    
                    if copies_available is not None and copies_available < 0:
                        print("\nError: Number of copies cannot be negative!")
                        continue
                    
                    if not any([title, author, isbn, published_year is not None, copies_available is not None]):
                        print("\nError: No fields to update! Please provide at least one value.")
                        continue
                    
                    updated = client.update_book(
                        book_id,
                        title=title,
                        author=author,
                        isbn=isbn,
                        published_year=published_year,
                        copies_available=copies_available
                    )
                    print("\n------- Book Updated Successfully! ------ \n")
                    print_book(updated, book_id)
                    
                except ValueError:
                    print("\nError: Year and Copies must be valid numbers!")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print(f"\nError: Failed to update book.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '5':
                try:
                    book_id = input("Book ID: ").strip()
                    
                    if not book_id:
                        print("\nError: Book ID cannot be empty!")
                        continue
                    
                    confirm = input(f"\nAre you sure you want to delete Book ID {book_id}? (yes/no): ").strip().lower()
                    
                    if confirm in ['yes', 'y']:
                        client.delete_book(book_id)
                        print("\n------- Book Deleted Successfully!")
                    else:
                        print("\n⚠ Deletion cancelled.")
                        
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print(f"\nError: Failed to delete book.")
                        print(f"Details: {error_msg}")
            
            else:
                print("\nInvalid choice! Please select a valid option.")
                
            input("\nPress Enter to continue... ")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            input("\nPress Enter to continue... ")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
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
        print("3. Search User Info")
        print("4. Update User Info")
        print("5. Delete User Info")
        print("b. Back\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'b':
            break
            
        try:
            if cmd == '1':
                try:
                    username = input("Username: ").strip()
                    full_name = input("Full Name: ").strip()
                    email = input("Email: ").strip()
                    
                    if not username or not full_name or not email:
                        print("\nError: Username, Full Name, and Email cannot be empty!")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    if '@' not in email or '.' not in email.split('@')[-1]:
                        print("\nError: Please enter a valid email address!")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    user = client.add_user(username, full_name, email)
                    print("\n------- User Added Successfully! ------\n")
                    print_user(user)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "409" in error_msg:
                        print("\nError: A user with this username already exists!")
                    else:
                        print(f"\nError: Failed to add user.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '2':
                try:
                    data = client.list_users()
                    users = data.get('users', data) if isinstance(data, dict) else data
                    
                    if not users or (isinstance(users, dict) and len(users) == 0):
                        print("\n👥 No users found in the system!")
                    else:
                        print("\n--- All Users ---")
                        if isinstance(users, dict):
                            for uid, u in sorted(users.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0]):
                                print_user(u, uid)
                        else:
                            for u in users:
                                print_user(u, u.get('id'))
                                
                except Exception as e:
                    print(f"\nError: Failed to retrieve users list.")
                    print(f"Details: {e}")
                        
            elif cmd == '3':
                try:
                    user_id = input("User ID: ").strip()
                    
                    if not user_id:
                        print("\nError: User ID cannot be empty!")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    user = client.get_user(user_id)
                    print("\n------- User Found! ------\n")
                    print_user(user)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: User not found!")
                        print("Please check if the User ID exists.")
                    else:
                        print(f"\nError: Failed to search for user.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '4':
                try:
                    user_id = input("User ID: ").strip()
                    
                    if not user_id:
                        print("\nError: User ID cannot be empty!")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    try:
                        existing_user = client.get_user(user_id)
                        print("\n--- Current User Details ---")
                        print_user(existing_user, user_id)
                    except Exception as e:
                        error_msg = str(e)
                        if "404" in error_msg:
                            print(f"\nError: User with ID '{user_id}' does not exist!")
                            print("Please check the User ID and try again.")
                        else:
                            print(f"\nError: Failed to retrieve user details.")
                            print(f"Details: {error_msg}")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    print("\n--- Update User ---")
                    print("Leave fields blank to keep current values:")
                    username = prompt("New Username: ")
                    full_name = prompt("New Full Name: ")
                    email = prompt("New Email: ")
                    
                    if email and ('@' not in email or '.' not in email.split('@')[-1]):
                        print("\nError: Please enter a valid email address!")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    if not any([username, full_name, email]):
                        print("\nError: No fields to update! Please provide at least one value.")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    updated = client.update_user(
                        user_id,
                        username=username,
                        full_name=full_name,
                        email=email
                    )
                    print("\n------- User Updated Successfully! ------\n")
                    print("\n--- Updated User Details ---")
                    print_user(updated, user_id)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: User not found!")
                        print("Please check if the User ID exists.")
                    elif "409" in error_msg:
                        print("\nError: Username already exists!")
                        print("Please choose a different username.")
                    else:
                        print(f"\nError: Failed to update user.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '5':
                try:
                    user_id = input("User ID: ").strip()
                    
                    if not user_id:
                        print("\nError: User ID cannot be empty!")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    try:
                        existing_user = client.get_user(user_id)
                        print("\n--- User to be Deleted ---")
                        print_user(existing_user, user_id)
                    except Exception as e:
                        error_msg = str(e)
                        if "404" in error_msg:
                            print(f"\nError: User with ID '{user_id}' does not exist!")
                            print("Please check the User ID and try again.")
                        else:
                            print(f"\nError: Failed to retrieve user details.")
                            print(f"Details: {error_msg}")
                        input("\nPress Enter to continue... ")
                        continue
                    
                    confirm = input(f"\nAre you sure you want to delete User ID {user_id} ({existing_user.get('username')})? (yes/no): ").strip().lower()
                    
                    if confirm in ['yes', 'y']:
                        client.delete_user(user_id)
                        print("\n------- User Deleted Successfully! -------\n")
                    else:
                        print("\nDeletion cancelled.")
                        
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: User not found!")
                        print("Please check if the User ID exists.")
                    else:
                        print(f"\nError: Failed to delete user.")
                        print(f"Details: {error_msg}")
            
            else:
                print("\nInvalid choice! Please select a valid option.")
                
            input("\nPress Enter to continue... ")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            input("\nPress Enter to continue... ")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            input("\nPress Enter to continue... ")

def borrow_return_menu():
    client = BorrowReturnClient("http://127.0.0.1:8000/borrow")
    
    while True:
        clear_screen()
        print("\n╔════════════════════════════════════╗")
        print("║  Borrow & Return System            ║")
        print("╚════════════════════════════════════╝")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. Track User's Borrowed Books")
        print("4. List All Borrowed Books")
        print("5. Check Book Availability")
        print("b. Back to Main Menu\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'b':
            break
            
        try:
            if cmd == '1':
                try:
                    user_id = int(input("Enter User ID: "))
                    book_id = int(input("Enter Book ID: "))
                    result = client.borrow_book(user_id, book_id)
                    print("\n------- Book Borrowed Successfully! -------\n")
                    print(f"Borrow ID: {result.get('borrow_id')}")
                    print(f"Book: {result.get('book_title')}")
                    print(f"Due Date: {result.get('due_date')}")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: User or Book not found.")
                        print("Please check if the User ID and Book ID exist.")
                    elif "400" in error_msg:
                        print("\nError: Book is not available for borrowing.")
                        print("All copies of the book are currently borrowed.")
                    else:
                        print(f"\nError: {error_msg}")
            elif cmd == '2':
                try:
                    borrow_id = int(input("Enter Borrow ID: "))
                    result = client.return_book(borrow_id)
                    print("\n ----- Book Returned Successfully! ----- \n")
                    print(f"Return Date: {result.get('return_date')}")
                    print(f"Book ID: {result.get('book_id')}")
                    print(f"User ID: {result.get('user_id')}")
                except ValueError:
                    print("\n Error: Please enter a valid numeric Borrow ID!")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\n Error: Borrow record not found!")
                        print("Please check if the Borrow ID exists.")
                    elif "400" in error_msg:
                        print("\n Error: This book has already been returned!")
                    else:
                        print(f"\n Error: {error_msg}")
                
            elif cmd == '3':
                try:
                    user_id = int(input("Enter User ID: "))
                    result = client.track_user_borrows(user_id)
                    print(f"\n--- User ID: {result.get('user_id')} ---")
                    print(f"Total Borrows: {result.get('total_borrows')}")
                    
                    borrows = result.get('borrows', [])
                    if borrows:
                        for borrow in borrows:
                            print_borrow(borrow)
                    else:
                        print("\nNo borrow records found for this user.")
                except ValueError:
                    print("\nError: Please enter a valid numeric User ID!")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: User not found!")
                        print("Please check if the User ID exists.")
                    else:
                        print(f"\nError: {error_msg}")
                
            elif cmd == '4':
                try:
                    result = client.list_borrowed_books()
                    print(f"\n--- Currently Borrowed Books ---")
                    print(f"Total: {result.get('total_borrowed')}")
                    
                    borrowed = result.get('borrowed_books', [])
                    if borrowed:
                        for borrow in borrowed:
                            print_borrow(borrow)
                    else:
                        print("\nNo books are currently borrowed. All books are available!")
                except Exception as e:
                    error_msg = str(e)
                    print(f"\n Error: Failed to retrieve borrowed books list.")
                    print(f"Details: {error_msg}")
            elif cmd == '5':
                try:
                    book_id = int(input("Enter Book ID: "))
                    result = client.check_book_availability(book_id)
                    print_availability(result)
                except ValueError:
                    print("\nError: Please enter a valid numeric Book ID!")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("\nError: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print(f"\nError: {error_msg}")
            
            else:
                print("Invalid choice!")
                
            input("\nPress Enter to continue... ")
            
        except ValueError:
            print("Error: Please enter valid numeric IDs!")
            input("\nPress Enter to continue... ")
        except Exception as e:
            print(f"Error: {e}")
            input("\nPress Enter to continue... ")

def main_menu():
    while True:
        clear_screen()
        print("\n╔════════════════════════════════════╗")
        print("║  Library Management System Client  ║")
        print("╚════════════════════════════════════╝")
        print("\n1. Book Management")
        print("2. User Management")
        print("3. Borrow & Return System")
        print("q. Quit\n")
        
        choice = input("Select Option: ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            sys.exit(0)
        elif choice == '1':
            book_management_menu()
        elif choice == '2':
            user_management_menu()
        elif choice == '3':
            borrow_return_menu()
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue... ")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)