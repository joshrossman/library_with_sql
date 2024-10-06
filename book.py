import my_users, regex
from connect_sql import my_connect
from datetime import date

class BookOpperations:
    #Create book object and add book object to libarary. Run new data through regex_checker to check that the user input is correct.
    author_id=''
    def set_book(conn,cursor):
        try:
            title=regex.regex_checker(input("Book Name:"),r"^[a-zA-Z1-9.%+-]{0,255}","Please input a valid book title")
            author=regex.regex_checker(input("Author:"),r"^[a-zA-Z]+\s*(a-zA-Z]+)?.*\s[A-Za-z]+$","Please input a valid name")
            isbn=regex.regex_checker(input("ISBN:"),r"^[0-9]{13}","Please input a valid 13 digit ISBN")
            publication_date=regex.regex_checker(input("Publication Date: YYYY-MM-DD:"),r"^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$","Please enter a valid date in the following format YYYY-MM-DD")
              
            try:
                query='SELECT id FROM authors WHERE name LIKE %s'
                cursor.execute(query,(author,))
                author_id=cursor.fetchall()[0][0]
                if not author_id:
                    author_id='error'
            except IndexError:
                print("Error:Author not in system. Could not create a new book.")
            except Exception as e:
                print(f"Error: {e}")
        
            try:
                query='SELECT isbn FROM books WHERE isbn = %s'
                cursor.execute(query,(isbn,))
                ISBN=cursor.fetchall()
               
                if author_id and not ISBN:
                    query='''INSERT INTO books(title,author_id,isbn,publication_date,availability) 
                    VALUES (%s,%s,%s,%s,%s);
                    '''
                    cursor.execute(query,(title,author_id,isbn,publication_date,1))
                    conn.commit()
                    print('Book Added.')
                elif author_id and ISBN:
                    print("Error: Cannot create new book entry. This ISBN is already in the system.")    
            except UnboundLocalError:
                #A 2nd error will be thrown if author is not in the database, so var author_id will not have any assigned value. This is to catch that exception, but no new message or fix is needed.
                pass     
            except Exception as e:
                print(f'Cannot create new book. Error:{e}')
        except Exception as e:
            print(f'Error:{e}')

    #Check if book is available. Create new column in table borrow_books to list borrowed book and user.    
    def borrow_book(conn,cursor):
        try:
            take_out_book=input("What book would you like to borrow?")
            query='SELECT * FROM books WHERE title=%s'
            cursor.execute(query,(take_out_book,))
            book_exsists=cursor.fetchall()
            if not book_exsists:
                print('Sorry, we could not find that book in our database.')
            else:
                book_available=book_exsists[0][5]
                if book_available==1:   
                    my_user=input('Which user is checking out this book?')
                    query='SELECT id FROM users WHERE name=%s'
                    cursor.execute(query,(my_user,))
                    user_id=cursor.fetchall()
                    if user_id:
                        query='''
                        INSERT INTO borrowed_books(user_id, book_id, borrow_date, return_date)
                        VALUES(%s,%s,%s,%s);
                        
                        '''
                        cursor.execute(query,(user_id[0][0],book_exsists[0][0],date.today(),'2020-12-12'))
                        conn.commit()
                        query='''
                        UPDATE books 
                        SET availability = 0
                        WHERE title = %s;
                        '''
                        cursor.execute(query,(book_exsists[0][1],))
                        conn.commit()
                        print(f'{book_exsists[0][1]} has been checked out to {my_user}')


                    else:
                        print('Sorry, we were not able to check out this book. That user is not in our system.')               
        
                else:
                    print('Sorry, that book has already been checked out. Please check back in a few weeks.')
        except Exception as e:
            print(f'Error:{e}')

    #Delete entry from Borrowed books table. Change book availability to available.          
    def return_book(conn,cursor):
        try:
            book_to_return=input("What book would you like to return?")
            query="SELECT id,availability FROM books WHERE title=%s"
            cursor.execute(query,(book_to_return,))
            book_id,book_availability=cursor.fetchall()[0]
            
            if book_id:
                if book_availability ==1:
                    print('Sorry, there seems to be a mistake. That book is not currently checked out of our system, so we cannot return it. Please see librarian to address issue.')
                else:
                    query='UPDATE books SET availability=1 WHERE title=%s;'
                    cursor.execute(query,(book_to_return,))
                    conn.commit()
                    query="DELETE FROM borrowed_books WHERE book_id=%s;"
                    cursor.execute(query,(book_id,))
                    conn.commit()
                    print(f"Your book {book_to_return} has been returned to the library.")
            else:
                print('Sorry, we could not find that book in our database. Please check book name and spelling')
        except Exception as e:
            print(f'Error:{e}')
        
    #Search library for a book. Return the book if found, or a message indicating that it was not found.
    def get_book(conn, cursor):
        my_book=input("What book would you like to search for?")
        try:
            query='SELECT * FROM books WHERE title = %s'
            cursor.execute(query,(my_book,))
            my_book=cursor.fetchall()
            if my_book:
                for row in my_book :
                    if row[5]==1:
                        availability='Available'
                    elif row[5]==0:
                        availability='Not Available'
                    print(f'Book ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, ISBN: {row[3]}, Publication Date: {row[4]}, Availability: {availability}')       
            else:
                print('Sorry, we could not find that book in our database.')
        except Exception as e:
            print("Sorry we could not find the book you are searching for in our database.")
      
    
    #Display all books in the library
    def get_books(conn,cursor):
        try:
            if conn:
                query='SELECT * FROM books'
                cursor.execute(query)
            for row in cursor.fetchall():
                if row[5]==1:
                    availability='Available'
                elif row[5]==0:
                    availability='Not Available'
                print(f'Book ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, ISBN: {row[3]}, Publication Date: {row[4]}, Availability: {availability}')
        except Exception as e:
            print('Error:{e}')

    #user interface for the BookOpperations class. Called from the main function.
    def UI_book_options():
        conn=my_connect()
        cursor=conn.cursor()
        while True:
            my_choice=input("Please choose an option by selecting the corresponding number:\n[1]Add a book to the library database\n[2]Check out a book\n[3]Return a book\n[4]Search for a book\n[5]Display all library books.\n[6]Return to main menu\nUser Input:")
            if my_choice=="1":
                BookOpperations.set_book(conn,cursor)
            elif my_choice=="2":
                BookOpperations.borrow_book(conn,cursor)
            elif my_choice=="3":
                BookOpperations.return_book(conn,cursor)
            elif my_choice=="4":
                BookOpperations.get_book(conn,cursor)
            elif my_choice=="5":
                BookOpperations.get_books(conn,cursor)
            elif my_choice=="6":
                if conn and conn.is_connected():
                    conn.close()
                    cursor.close()
                break
            else:
                print("Not a valid choice. Please try again.")