import os
from book_management import BookManagementClient, print_book
from user_management import UserManagementClient, print_user
from borrow_return import BorrowReturnClient, print_borrow
from admin import (AdminClient, print_full_report, print_summary, print_overdue_report, print_most_borrowed_report, print_borrowing_history)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def book_management_menu():
    client = BookManagementClient("http://127.0.0.1:8000/book")
    
    while True:
        clear_screen()
        print("╔════════════════════════════════════╗")
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
                    book = client.add_book(title, author, isbn, year, copies)
                    print("Book Added Successfully!")
                    print_book(book)
                    
                except ValueError:
                    print("Error: Year and Copies must be valid numbers!")
                except Exception as e:
                    error_msg = str(e)
                    if "409" in error_msg:
                        print("Error: A book with this ISBN already exists!")
                    else:
                        print("Error: Failed to add book.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '2':
                try:
                    data = client.list_books()
                    books = data.get('books', data) if isinstance(data, dict) else data
                    
                    if not books or (isinstance(books, dict) and len(books) == 0):
                        print("No books found in the library!")
                    else:
                        print("All Books")
                        if isinstance(books, dict):
                            for bid, b in sorted(books.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0]):
                                print_book(b, bid)
                        else:
                            for b in books:
                                print_book(b, b.get('id'))
                                
                except Exception as e:
                    print("Error: Failed to retrieve books list.")
                    print(f"Details: {e}")
                        
            elif cmd == '3':
                try:
                    book_id = input("Book ID: ").strip()
                    
                    if not book_id:
                        print("Error: Book ID cannot be empty!")
                        continue
                    
                    book = client.get_book(book_id)
                    print("Book Found!")
                    print_book(book)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print("Error: Failed to search for book.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '4':
                try:
                    book_id = input("Book ID: ").strip()
                    
                    if not book_id:
                        print("Error: Book ID cannot be empty!")
                        continue

                    try:
                        existing_book = client.get_book(book_id)
                        print("Current Book Details")
                        print_book(existing_book, book_id)
                    except Exception as e:
                        if "404" in str(e):
                            print(f"Error: Book with ID '{book_id}' does not exist!")
                            print("Please check the Book ID and try again.")
                        else:
                            print("Error: Unable to retrieve book details.")
                            print(f"Details: {e}")
                        input("Press Enter to continue... ")
                        continue
                    
                    print("Leave fields blank to keep current values:")
                    title = input("Title: ")
                    author = input("Author: ")
                    isbn = input("ISBN: ")
                    published_year = int(input("Year: ")) 
                    copies_available = int(input("Copies: ")) 
                    
                    if not any([title, author, isbn, published_year is not None, copies_available is not None]):
                        print("Error: No fields to update! Please provide at least one value.")
                        continue
                    
                    updated = client.update_book(
                        book_id,
                        title=title,
                        author=author,
                        isbn=isbn,
                        published_year=published_year,
                        available_copies=copies_available
                    )

                    print("Book Updated Successfully!")
                    print_book(updated, book_id)
                    
                except ValueError:
                    print("Error: Year and Copies must be valid numbers!")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print("Error: Failed to update book.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '5':
                try:
                    book_id = input("Book ID: ").strip()
                    
                    if not book_id:
                        print("Error: Book ID cannot be empty!")
                        continue
                    
                    confirm = input(f"Are you sure you want to delete Book ID {book_id}? (yes/no): ").strip().lower()
                    
                    if confirm in ['yes', 'y']:
                        client.delete_book(book_id)
                        print("Book Deleted Successfully!")
                    else:
                        print("Deletion cancelled.")
                        
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: Book not found!")
                        print("Please check if the Book ID exists.")
                    else:
                        print("Error: Failed to delete book.")
                        print(f"Details: {error_msg}")
            
            else:
                print("Invalid choice! Please select a valid option.")
                
            input("Press Enter to continue... ")
            
        except KeyboardInterrupt:
            print("Operation cancelled.")
            input("Press Enter to continue... ")
        except Exception as e:
            print(f"Unexpected error: {e}")
            input("Press Enter to continue... ")

def user_management_menu():
    client = UserManagementClient("http://127.0.0.1:8000/user")
    
    while True:
        clear_screen()
        print("╔════════════════════════════════════╗")
        print("║  User Management                   ║")
        print("╚════════════════════════════════════╝")
        print("1. Add User")
        print("2. List Users")
        print("3. Search User Info")
        print("4. Update User Info")
        print("5. Delete User Info")
        print("b. Back")
        
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
                        print("Error: Username, Full Name, and Email cannot be empty!")
                        input("Press Enter to continue... ")
                        continue
                    
                    if '@' not in email or '.' not in email.split('@')[-1]:
                        print("Error: Please enter a valid email address!")
                        input("Press Enter to continue... ")
                        continue
                    
                    user = client.add_user(username, full_name, email)
                    print("User Added Successfully!")
                    print_user(user)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "409" in error_msg:
                        print("Error: A user with this username already exists!")
                    else:
                        print("Error: Failed to add user.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '2':
                try:
                    data = client.list_users()
                    users = data.get('users', data) if isinstance(data, dict) else data
                    
                    if not users or (isinstance(users, dict) and len(users) == 0):
                        print("No users found in the system!")
                    else:
                        print("All Users")
                        if isinstance(users, dict):
                            for uid, u in sorted(users.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0]):
                                print_user(u, uid)
                        else:
                            for u in users:
                                print_user(u, u.get('id'))
                                
                except Exception as e:
                    print("Error: Failed to retrieve users list.")
                    print(f"Details: {e}")
                        
            elif cmd == '3':
                try:
                    user_id = input("User ID: ").strip()
                    
                    if not user_id:
                        print("Error: User ID cannot be empty!")
                        input("Press Enter to continue... ")
                        continue
                    
                    user = client.get_user(user_id)
                    print(" User Found!")
                    print_user(user)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: User not found!")
                        print("Please check if the User ID exists.")
                    else:
                        print("Error: Failed to search for user.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '4':
                try:
                    user_id = input("User ID: ").strip()
                    
                    if not user_id:
                        print("Error: User ID cannot be empty!")
                        input("Press Enter to continue... ")
                        continue
                    
                    try:
                        existing_user = client.get_user(user_id)
                        print("Current User Details")
                        print_user(existing_user, user_id)
                    except Exception as e:
                        error_msg = str(e)
                        if "404" in error_msg:
                            print(f"Error: User with ID '{user_id}' does not exist!")
                            print("Please check the User ID and try again.")
                        else:
                            print("Error: Failed to retrieve user details.")
                            print(f"Details: {error_msg}")
                        input("Press Enter to continue... ")
                        continue
                    
                    print("Update User Info")
                    print("Leave fields blank to keep current values:")
                    username = input("New Username: ")
                    full_name = input("New Full Name: ")
                    email = input("New Email: ")
                    
                    if email and ('@' not in email or '.' not in email.split('@')[-1]):
                        print("Error: Please enter a valid email address!")
                        input("Press Enter to continue... ")
                        continue
                    
                    if not any([username, full_name, email]):
                        print("Error: No fields to update! Please provide at least one value.")
                        input("Press Enter to continue... ")
                        continue
                    
                    updated = client.update_user(user_id, username=username, full_name=full_name, email=email)
                    print("User Updated Successfully!")
                    print("Updated User Details:")
                    print_user(updated, user_id)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: User not found!")
                        print("Please check if the User ID exists.")
                    elif "409" in error_msg:
                        print("Error: Username already exists!")
                        print("Please choose a different username.")
                    else:
                        print("Error: Failed to update user.")
                        print(f"Details: {error_msg}")
                
            elif cmd == '5':
                try:
                    user_id = input("User ID: ").strip()
                    
                    if not user_id:
                        print("Error: User ID cannot be empty!")
                        input("Press Enter to continue... ")
                        continue
                    
                    try:
                        existing_user = client.get_user(user_id)
                        print("User to be Deleted")
                        print_user(existing_user, user_id)
                    except Exception as e:
                        error_msg = str(e)
                        if "404" in error_msg:
                            print(f"\nError: User with ID '{user_id}' does not exist!")
                            print("Please check the User ID and try again.")
                        else:
                            print("Error: Failed to retrieve user details.")
                            print(f"Details: {error_msg}")
                        input("Press Enter to continue... ")
                        continue
                    
                    username = existing_user.get('username') if existing_user else 'Unknown'
                    confirm = input(f"Are you sure you want to delete User ID {user_id} ({username})? (yes/no): ").strip().lower()
                    
                    if confirm in ['yes', 'y']:
                        client.delete_user(user_id)
                        print("User Deleted Successfully!")
                    else:
                        print("Deletion cancelled.")
                        
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: User not found!")
                        print("Please check if the User ID exists.")
                    else:
                        print("Error: Failed to delete user.")
                        print(f"Details: {error_msg}")
            
            else:
                print("Invalid choice! Please select a valid option.")
                
            input("Press Enter to continue... ")
            
        except KeyboardInterrupt:
            print("Operation cancelled.")
            input("Press Enter to continue... ")
        except Exception as e:
            print(f"Unexpected error: {e}")
            input("Press Enter to continue... ")

def borrow_return_menu():
    client = BorrowReturnClient("http://127.0.0.1:8000/borrow")
    
    while True:
        clear_screen()
        print("╔════════════════════════════════════╗")
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
                    print("Book Borrowed Successfully!")
                    if result:
                        print(f"Borrow ID: {result.get('borrow_id')}")
                        print(f"Book ID: {result.get('book_id')}")
                        print(f"Due Date: {result.get('due_date')}")
                    else:
                        print("Book borrowed, but no details returned.")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: User or Book not found.")
                    elif "400" in error_msg:
                        print("Error: Book is not available for borrowing.")
                    elif "409" in error_msg:
                        print("Error: User has already borrowed this book.")
                    else:
                        print(f"Error: {error_msg}")

            elif cmd == '2':
                try:
                    user_id = int(input("Enter User ID: "))
                    book_id = int(input("Enter Book ID: "))
                    result = client.return_book(user_id, book_id)
                    print("Book Returned Successfully!")
                    if result:
                        print(f"Return Date: {result.get('return_date')}")
                        print(f"Book ID: {result.get('book_id')}")
                        print(f"User ID: {result.get('user_id')}")
                    else:
                        print("Book returned, but no details returned.")
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        print("Error: Borrow record not found!")
                    elif "400" in error_msg:
                        print("Error: This book has already been returned!")
                    else:
                        print(f"Error: {error_msg}")

            elif cmd == '3':
                try:
                    user_id = int(input("Enter User ID: "))
                    borrows = client.track_user_borrows(user_id)

                    if borrows is None:
                        borrows = []
                    
                    borrowed_only = [b for b in borrows if b.get('status') == 'borrowed']

                    if borrowed_only:
                        print(f"Borrow Records for User ID: {user_id}")
                        for borrow in borrowed_only:
                            print_borrow(borrow)
                    else:
                        print("No borrow records found for this user.")
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == '4':
                try:
                    all_borrows = client.list_borrows()
                    
                    if all_borrows is None:
                        all_borrows = []

                    borrowed_only = [b for b in all_borrows if b.get('status') == 'borrowed']
                    if borrowed_only:
                        print("All Borrowed Books")
                        for borrow in borrowed_only:
                            print_borrow(borrow)
                    else:
                        print("No books are currently borrowed. All books are available!")
                except Exception as e:
                    print(f"Error: Failed to retrieve borrowed books list. Details: {e}")
                    
            elif cmd == '5':
                try:
                    book_id = int(input("Enter Book ID: "))
                    availability = client.check_book_availability(book_id)
                    print(f"Book ID: {book_id}")
                    if availability:
                        print(f"Available Copies: {availability.get('available_copies')}")
                    else:
                        print("Available Copies: No data available")
                except Exception as e:
                    print(f"\nError: {e}")
                    
            else:
                print("Invalid choice! Please select a valid option.")
                
            input("Press Enter to continue... ")
            
        except ValueError:
            print("Error: Please enter valid numeric IDs!")
            input("Press Enter to continue... ")
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter to continue... ")

def admin_reports_menu():
    client = AdminClient("http://127.0.0.1:8000/admin")
    
    while True:
        clear_screen()
        print("╔════════════════════════════════════╗")
        print("║  Admin Reports & Analytics         ║")
        print("╚════════════════════════════════════╝")
        print("1. View Complete System Report")
        print("2. View Summary Statistics")
        print("3. View Overdue Books")
        print("4. View Most Borrowed Books")
        print("5. View Borrowing History")
        print("6. View User-Specific Borrowing History")
        print("b. Back to Main Menu\n")
        
        cmd = input("Choice: ").strip().lower()
        
        if cmd == 'b':
            break
            
        try:
            if cmd == '1':
                try:
                    report = client.get_all_reports()
                    print_full_report(report)
                except Exception as e:
                    print("Error: Failed to retrieve system report.")
                    print(f"Details: {e}")
            
            elif cmd == '2':
                try:
                    report = client.get_all_reports()
                    if report and 'summary' in report:
                        print_summary(report['summary'])
                    else:
                        print("Error: Summary data not available.")
                except Exception as e:
                    print("Error: Failed to retrieve summary statistics.")
                    print(f"Details: {e}")
            
            elif cmd == '3':
                try:
                    overdue = client.get_overdue_books()
                    print_overdue_report(overdue)
                except Exception as e:
                    print("Error: Failed to retrieve overdue books.")
                    print(f"Details: {e}")
            
            elif cmd == '4':
                try:
                    most_borrowed = client.get_most_borrowed_books()
                    print_most_borrowed_report(most_borrowed)
                except Exception as e:
                    print("Error: Failed to retrieve most borrowed books.")
                    print(f"Details: {e}")
            
            elif cmd == '5':
                try:
                    history = client.get_borrowing_history()
                    print_borrowing_history(history)
                except Exception as e:
                    print("Error: Failed to retrieve borrowing history.")
                    print(f"Details: {e}")
            
            elif cmd == '6':
                try:
                    user_id = int(input("Enter User ID: "))
                    history = client.get_borrowing_history(user_id)
                    
                    if history:
                        print(f"Borrowing History for User ID: {user_id}")
                        print_borrowing_history(history)
                    else:
                        print(f"No borrowing history found for User ID: {user_id}")
                        
                except ValueError:
                    print("Error: Please enter a valid User ID (number)!")
                except Exception as e:
                    print("Error: Failed to retrieve user borrowing history.")
                    print(f"Details: {e}")
            
            else:
                print("Invalid choice! Please select a valid option.")
                
            input("Press Enter to continue... ")
            
        except KeyboardInterrupt:
            print("nOperation cancelled.")
            input("Press Enter to continue... ")
        except Exception as e:
            print(f"Unexpected error: {e}")
            input("Press Enter to continue... ") 
            
def main_menu():
    while True:
        clear_screen()
        print("╔════════════════════════════════════╗")
        print("║  Library Management System Client  ║")
        print("╚════════════════════════════════════╝")
        print("1. Book Management")
        print("2. User Management")
        print("3. Borrow & Return System")
        print("4. Admin Reports & Analytics")
        print("q. Quit")
        
        choice = input("Select Option: ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == '1':
            book_management_menu()
        elif choice == '2':
            user_management_menu()
        elif choice == '3':
            borrow_return_menu()
        elif choice == '4':
            admin_reports_menu()
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue... ")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("Exiting...")