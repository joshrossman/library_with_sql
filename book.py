import my_users, regex, books_to_sql as b_t_s

class BookOpperations:
    def __init__(self, title, author,  genre, publication_date, available,*on_loan_to):
        self._title=title
        self._author=author
        self._genre=genre
        self._publication_date=publication_date
        self.availability=available
        self.on_loan_to=on_loan_to

    #Create book okbject and add book object to libarary. Run new data through regex_checker to check that the user input is correct.
    def set_book(library):
        title=regex.regex_checker(input("Book Name:"),r"^[a-zA-Z1-9.%+-]+","Please input a valid book title")
        author=regex.regex_checker(input("Author:"),r"^[a-zA-Z]+\s*(a-zA-Z]+)?.*\s[A-Za-z]+$","Please input a valid name")
        genre=regex.regex_checker(input("Genre:"),r"^[a-zA-Z\s]+$","Please input a valid genre")
        publication_date=regex.regex_checker(input("Publication Date: YYYY-MM-DD:"),r"^[1-2][0-9][0-9][0-9]-[0-3][0-9]-[0-1][0-9]$","Please enter a valid date in the following format YYYY-MM-DD")
        library.append(BookOpperations(title,author,genre,publication_date,"Available"))
        b_t_s.book_to_database(title,author,12345,publication_date,1)
     ###############fix ISBN- fix publication date?#########  
    #function to borrow book. Changes status of book to borrowed and adds a User object to "on_loan_to", to keep track of who currently has the book.         
    def borrow_book(library, *users):
        in_database=False
        is_available=False
        if len(users[0])>=1:
            my_book=input("What book would you like to take out?")
            for book in library:
                if my_book.lower() ==book._title.lower():
                    in_database=True
                    if book.availability=="Available":
                        in_database=True
                        book.availability="Borrowed"
                        #runs a borrow book function with a UserOperations object, to keep track of which books a user currently has.
                        my_user=my_users.UserOperations.borrow_book(users,book)
                        book.on_loan_to=my_user
                        print(f"{book._title} is currently available, and is being checked out to {my_user.name}")
                        return in_database, is_available,book,library     
            if in_database and not is_available:
                print("We do carry this book in our library. However, the book is currently checked out. Please check back in a few days and it may be avialable.")
            if not in_database:
                print("Sorry, but we could not find that title in our library database.")
        else:
            print("We cannot check out any books, as there are currently no users listed in our database. Please first add a user into the system.")      
            
    #Function to return a book to the libary. Changes status to avialbable. Removes the User object from "on_loan_to", and runs the return book function of the UserOpertations object.
    def return_book(library):
        my_book=input("What book are you returning?")
        is_found=False
        is_available=False
        for book in library:
            if my_book.lower()==book._title.lower():
                is_found=True
                my_book=book._title
                if book.availability=="Borrowed":
                    is_available=True
                    print(f"Thank you for returning {book._title} to the library!")
                    book.availability="Available"
                    my_users.UserOperations.return_book(book.on_loan_to,book._title)
                    book.on_loan_to=''
                    return library,is_found,is_available
        if is_found and not is_available:  
            print(f"Thank you for trying to return {my_book}. According to our records, that book has not been checked out. Perhaps you are returning it to the wrong library.")
        if not is_found:
            print("We do not have that book in our database. Please check spelling to ensure you are searching correctly.")
    
    #Search library for a book. Return the book if found, or a message indicating that it was not found.
    def get_book(library):
        my_book=input("What book would you like to search for?")
        is_found=False
        for book in library:
            if my_book.lower()==book._title.lower():
                is_found=True
                print(f"\nTitle:{book._title},\nAuthor:{book._author},\nGenre:{book._genre},\nPublication Date:{book._publication_date}\nAvailabiliy: {book.availability}")
                return is_found
        if not is_found:
            print("Sorry we could not find the book you are searching for in our database.")

    #Display all books in the library
    def gets_books(library):
        for book in library:
            print(f"\nTitle:{book._title},\nAuthor:{book._author},\nGenre:{book._genre},\nPublication Date:{book._publication_date}\nAvailabiliy: {book.availability}")

    #user interface for the BookOpperations object. Called from the main function. Writes to the user and book doc after a given oppertation.
    def UI_book_options(library,users):
        while True:
            my_choice=input("Please choose an option by selecting the corresponding number:\n[1]Add a book to the library database\n[2]Check out a book\n[3]Return a book\n[4]Search for a book\n[5]Display all library books.\n[6]Return to main menu\nUser Input:")
            if my_choice=="1":
                BookOpperations.set_book(library)
            elif my_choice=="2":
                BookOpperations.borrow_book(library,users)
            elif my_choice=="3":
                BookOpperations.return_book(library)
            elif my_choice=="4":
                BookOpperations.get_book(library)
            elif my_choice=="5":
                BookOpperations.get_books(library)
            elif my_choice=="6":
                break
            else:
                print("Not a valid choice. Please try again.")