import random
from connect_sql import my_connect
class UserOperations:
    
    #Creates a new user and inserts into SQL table. Check to make sure user does not already exsist.       
    def new_user(con,cursor):
        name=input("Please enter new user's full name:")
        
        try:
            query='SELECT * FROM users WHERE name=%s'
            cursor.execute(query,(name,))

            if not cursor.fetchall():
                lib_id=UserOperations.create_lib_id(con,cursor)
                query='INSERT INTO users(name,library_id) VALUES(%s,%s)'
                cursor.execute(query,(name,lib_id))
                con.commit()
                print(f"\nNew User Created!\nName: {name}\nID:{lib_id}")

            else:
                print(f"Cannot create account. This patron already has a library account.")
       
        except Exception as e:
            print(f"Error:{e}") 

    #Creates a unique random user ID for new user.    
    def create_lib_id(con,cursor):
        try:
            while True:  
                max=9999999999
                lib_id=str(random.randint(0,max))
                floating_zero_filler=''
                for i in range(10-len(lib_id)):
                    floating_zero_filler+='0'
                lib_id=floating_zero_filler+lib_id
                
                query='SELECT * FROM users WHERE library_id =%s'
                cursor.execute(query,(lib_id,))
                if len(cursor.fetchall())==max:
                    raise NoIdsAvailable("All available IDs have been used. Please consider clearing old users/ID, or adjusting program to allow more numbers to be generated(not reccomended.)")     
                if not cursor.fetchall():
                    return lib_id
        except Exception as e:
            print(f'Error:{e}')
            
    # Display a users information based on user input.                    
    def user_details(conn,cursor):
        try:
            query='SELECT * FROM users'
            cursor.execute(query)
            if cursor.fetchall():
                my_user=input("Which user would you like to retrieve information about?")
                query='SELECT * FROM users WHERE name=%s'
                cursor.execute(query,(my_user,))
                my_user=cursor.fetchall()
                if my_user:
                    for user in my_user:
                        print(f'Database ID: {user[0]}\nName: {user[1]}\nLibrary ID {user[2]}\n')
                else:
                    print("Sorry we could not find that use in our database.")
    
            else:
                print("There are currently no users in the system to display.")
        except Exception as e:
            print(f'Error:{e}')

    #Diplays details of all users.
    def display_all(conn,cursor):
        try:
            query='SELECT * FROM users'
            cursor.execute(query)
            the_users=cursor.fetchall()
            if the_users:    
                for user in the_users:
                    print(f"\nDatabase ID: {user[0]}\nName:{user[1]}\nLibrary ID:{user[2]}")
            else:
                print("There are currently no users in the system to display.")
        except Exception as e:
            print(f'Error:{e}')

    #User interfact of UserOperations object
    def UI_user_operations():
        conn=my_connect()
        cursor=conn.cursor()
        while True:
            my_choice=input("Please choose an option by selecting the corresponding number:\n[1]Add a new user\n[2]Display user details\n[3]Display all users\n[4]Return to main menu\nUser Input:")
            if my_choice=="1":
                UserOperations.new_user(conn,cursor)
            elif my_choice=="2":
                UserOperations.user_details(conn,cursor)
            elif my_choice=="3":
                UserOperations.display_all(conn,cursor)
            elif my_choice=="4":
                if conn and conn.is_connected():
                    conn.close()
                    cursor.close()
                break
            else:
                print("Not a valid choice. Please try again.")
            

# Creates error if no more unique IDs able to be created       
class NoIdsAvailable(Exception):
    def __init__(self,error):
        print(error)