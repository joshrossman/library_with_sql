import random
class UserOperations:
    def __init__(self,name,lib_id,borrowed_books):
        self.name=name
        self.lib_id=lib_id
        self.borrowed_books=borrowed_books

    #Keeps track of borrowed books in a list "borrowed_books"
    def borrow_book(users,book):
        while True:
            user_name=input("Please enter the name of the user that is checking out this book:")
            for user in users:
                for my_keys, my_items in user.items():
                    if my_items[0].lower() ==user_name.lower():
                        my_items[2].append(book._title)
                        return my_keys
                    else:
                        continue
            print("Sorry, we could not find that user in our database!")

    #removes borrowed books from list borrowed_books                            
    def return_book(users,book):
        if type(users)==tuple:    
            my_index=users[0].borrowed_books.index(book)
            users[0].borrowed_books.pop(my_index)
            return users[0].name
        else:
            my_index=users.borrowed_books.index(book)
            users.borrowed_books.pop(my_index)
            return users.name

    #Creates a new user Object. Var in_users used to check if user already exsists in list.       
    def new_user(users):
        name=input("Please enter new user's full name:")
        in_users=False
        for user in users:  
            if user.name.lower()==name.lower():  
                in_users=True
                new_user=user

        if in_users==False:   
            new_user=UserOperations(name,UserOperations.create_lib_id(users),[])
            users[new_user]=(new_user.name,new_user.lib_id,new_user.borrowed_books)
            print(f"\nNew User Created!\nName: {new_user.name}\nID:{new_user.lib_id}")
            return users
        else:
            print(f"Cannot create account. This patron already has a library account.\nAccount number: {new_user.lib_id}") 

    #Creates a unique random user ID for new user.    
    def create_lib_id(users):
        while True:  
            max=9999999999
            if len(users)==max:
                raise NoIdsAvailable("All available IDs have been used. Please consider clearing old users/ID, or adjusting program to allow more numbers to be generated(not reccomended.)")     
            lib_id=str(random.randint(0,max))
            floating_zero_filler=''
            for i in range(10-len(lib_id)):
                floating_zero_filler+='0'
            lib_id=floating_zero_filler+lib_id
            lib_ids=[users.values()]
            if not lib_id in lib_ids:
                return lib_id
    #Printe all user details including name, user ID and borrowed books.                         
    def user_details(users):
        in_users=False
        if len(users)>0:
            my_user=input("Which user would you like to retrieve information about?")
            for userinfo in users.values():
                my_books=''
                for book in userinfo[2]:
                    my_books+="\n"+book
                if userinfo[0].lower()==my_user.lower():
                    print(f"\nUser:{userinfo[0]}\nUser ID:{userinfo[1]}\nBorrowed Books:{my_books}")
                    in_users=True
            if in_users==False:
                print("Sorry, but we could not find that user in our system.")
                
        else:
            print("There are currently not users in the system to display.")

    #Diplays details of all users.
    def display_all(users):
        if len(users)>0:
            for user, userinfo in users.items():
                my_books=''
                for book in user.borrowed_books:
                    my_books+=("\n" +book)
                print(f"\nUser: {userinfo[0]}\nLibrary Id:{userinfo[1]}\nBorrowed Books:{my_books}")
        else:
            print("There are currently no users in the system to display.")

    #User interfact of UserOperations object
    def UI_user_operations(users):
        while True:
            my_choice=input("Please choose an option by selecting the corresponding number:\n[1]Add a new user\n[2]Display user details\n[3]Display all users\n[4]Return to main menu\nUser Input:")
            if my_choice=="1":
                UserOperations.new_user(users)
            elif my_choice=="2":
                UserOperations.user_details(users)
            elif my_choice=="3":
                UserOperations.display_all(users)
            elif my_choice=="4":
                break
            else:
                print("Not a valid choice. Please try again.")
            

# Creates error if no more unique IDs able to be created       
class NoIdsAvailable(Exception):
    def __init__(self,error):
        print(error)