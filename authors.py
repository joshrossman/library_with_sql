class AuthorOperations:
    def __init__(self, name, biography):
        self.name=name
        self.biography = biography

    #creates a new author and biography
    def add_author(authors):
        author=input("What is the name of the author?")
        biography=input("Please include a short biography about the author:")
        authors.append(AuthorOperations(author, biography))
       

    #Displays author information
    def view_details(authors):
        my_author=input("What is the name of the author you would like to search for?")
        in_database=False
        for author in authors:
            if author.name.lower()==my_author.lower():
                in_database=True
                print(f"\nAuthor's name:{my_author}\nBiography:{author.biography}\n")
        if not in_database:
            print("Sorry, we do not have any information about that author in our database!")

    #Displays information of all authors in the system.
    def diplay_all(authors):
        for author in authors:
            print(f"Author: {author.name}\nBiography:{author.biography}")

    #User interface for Authors object
    def UI_Author_Operations(authors):
        while True:  
            my_choice=input("What would you like to do?\n[1]Add new author information\n[2]Search for an author\n[3]Print all authors\n[4]Return to main menu\nUser Input:")
            if my_choice=="1":
                AuthorOperations.add_author(authors)
            elif my_choice=="2":
                AuthorOperations.view_details(authors)
            elif my_choice=="3":
                AuthorOperations.diplay_all(authors)
            elif my_choice=="4":
                break
            else:
                print("Not a valid choice. Please choose from the listed menu items.")


