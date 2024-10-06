from connect_sql import my_connect
class AuthorOperations:
    #creates a new author and biography
    def add_author(conn,cursor):
        try:
            author=input("What is the name of the author?")
            biography=input("Please include a short biography about the author:")
            query='SELECT*FROM authors WHERE name=%s'
            cursor.execute(query,(author,))
            new_author=cursor.fetchall()
            if not new_author:    
                query="INSERT INTO authors(name,biography) VALUE(%s,%s);"
                cursor.execute(query,(author,biography))
                conn.commit()
                print("New author successfully added to database.")  
            else:
                print('Sorry, we could not add that author, they already exsist in our database')
        except Exception as e:
            print(f"Error:{e}.")
 

    #Displays author information
    def view_details(conn,cursor):
        try:
            my_author=input("What is the name of the author you would like to search for?")
            query='SELECT * FROM authors WHERE name=%s'
            cursor.execute(query,(my_author,))
            print_author=cursor.fetchall()
            if print_author:
                for author in print_author:
                    print(f"\nDatabase ID: {author[0]}\nAuthor's name:{author[1]}\nBiography:{author[2]}\n")
            else:
                print("Sorry, we do not have any information about that author in our database!")
        except Exception as e:
            print(f'Error:{e}')

    #Displays information of all authors in the system.
    def diplay_all(conn,cursor):
        try:
            query="SELECT * FROM authors"
            cursor.execute(query)
            print_authors=cursor.fetchall()
            if print_authors:
                for author in print_authors:
                    print(f'Database ID: {author[0]}\nAuthor:{author[1]}\nBiography:{author[2]}\n')
            else:
                print('Sorry, there are not authors in the database to print.')
        except Exception as e:
            print(f'Error:{e}')

    #User interface for Authors object
    def UI_Author_Operations():
        conn=my_connect()
        cursor=conn.cursor()
        while True:  
            my_choice=input("What would you like to do?\n[1]Add new author information\n[2]Search for an author\n[3]Print all authors\n[4]Return to main menu\nUser Input:")
            if my_choice=="1":
                AuthorOperations.add_author(conn,cursor)
            elif my_choice=="2":
                AuthorOperations.view_details(conn,cursor)
            elif my_choice=="3":
                AuthorOperations.diplay_all(conn,cursor)
            elif my_choice=="4":
                if conn and conn.is_connected():
                    conn.close()
                    cursor.close()
                break
            else:
                print("Not a valid choice. Please choose from the listed menu items.")


