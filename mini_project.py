import book, my_users, authors


#Main funtion and main user interface        
def main():
    while True:
        my_choice=input("Welcome to the Library Management System!Main Menu:\n[1]Book Operations\n[2]User Operations\n[3]Author Operations\n[4]Quit\nUser Input:")
        if my_choice=='1':
            book.BookOpperations.UI_book_options()  
        elif my_choice=='2':
            my_users.UserOperations.UI_user_operations()
        elif my_choice=='3':
            authors.AuthorOperations.UI_Author_Operations()
        elif my_choice=='4':
            print("Have a great day! Thank you for using the library system!")  
            break  

if __name__=="__main__": 
    main()






