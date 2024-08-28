import mysql.connector
import re
from tabulate import tabulate
from datetime import date, datetime, timedelta

databaseobj = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ragul',
    database='library'
)
login = databaseobj.cursor()

# Creating database library
login.execute("CREATE DATABASE IF NOT EXISTS library")

# Creating table role in database library
login.execute("CREATE TABLE IF NOT EXISTS role ("
              "role_id INT AUTO_INCREMENT PRIMARY KEY,"
              "role_name VARCHAR(50))")

# Inserting values into role table
insert_query = "INSERT INTO role (role_name) VALUES (%s)"
roles = [("admin",), ("user",)]
login.executemany(insert_query, roles)
databaseobj.commit()

# Creating table Users in database library
login.execute("CREATE TABLE IF NOT EXISTS Users ("
              "userid VARCHAR(50) PRIMARY KEY,"
              "first_name VARCHAR(50),"
              "last_name VARCHAR(50),"
              "mobile_number VARCHAR(10),"
              "email_id VARCHAR(50),"
              "username VARCHAR(50),"
              "password VARCHAR(50),"
              "role_id INT,"
              "FOREIGN KEY(role_id) REFERENCES role(role_id))")

# Creating table genre in database library
login.execute("CREATE TABLE IF NOT EXISTS genre ("
              "genre_id INT AUTO_INCREMENT PRIMARY KEY,"
              "genre_name VARCHAR(50))")

# Creating table author in database library
login.execute("CREATE TABLE IF NOT EXISTS author ("
              "author_id INT AUTO_INCREMENT PRIMARY KEY,"
              "author_name VARCHAR(50))")

# Creating table Books in database library
login.execute("CREATE TABLE IF NOT EXISTS Books ("
              "book_id INT AUTO_INCREMENT PRIMARY KEY,"
              "book_title VARCHAR(50),"
              "author VARCHAR(50),"
              "genre VARCHAR(50),"
              "published_year INT,"
              "author_id INT,"
              "genre_id INT,"
              "price INT,"
              "FOREIGN KEY(author_id) REFERENCES author(author_id),"
              "FOREIGN KEY(genre_id) REFERENCES genre(genre_id))")

# Creating table Membership in database library
login.execute("CREATE TABLE IF NOT EXISTS Membership ("
              "mem_id INT AUTO_INCREMENT PRIMARY KEY,"
              "membership_plan VARCHAR(50),"
              "start_date DATE,"
              "end_date DATE,"
              "user_id VARCHAR(50),"
              "FOREIGN KEY(user_id) REFERENCES Users(userid))")

# Creating table Payment in database library
login.execute("CREATE TABLE IF NOT EXISTS Payment ("
              "payment_id INT AUTO_INCREMENT PRIMARY KEY,"
              "payment_method VARCHAR(50),"
              "payment_date DATE,"
              "amount DECIMAL(10, 2),"
              "user_id VARCHAR(50),"
              "FOREIGN KEY(user_id) REFERENCES Users(userid))")

# Creating table Rent in database library
login.execute("CREATE TABLE IF NOT EXISTS Rent ("
              "rent_id INT AUTO_INCREMENT PRIMARY KEY,"
              "rent_amount DECIMAL(10, 2),"
              "rent_start_date DATE,"
              "rent_end_date DATE,"
              "user_id VARCHAR(50),"
              "book_id INT,"
              "FOREIGN KEY(user_id) REFERENCES Users(userid),"
              "FOREIGN KEY(book_id) REFERENCES Books(book_id))")
# Creating table Listofusers in database library
login.execute("CREATE TABLE IF NOT EXISTS listofusers ("
              "Uid VARCHAR(50),"
              "UNAME VARCHAR(50),"
              "Currentpassword VARCHAR(50),"
              "Membershipid VARCHAR(50), "
              "Plan_currently VARCHAR(50),"
              "Pending_dues VARCHAR(50))")
# Creating table overduebooks in database library
"""login.execute("CREATE TABLE IF NOT EXISTS overduebooks ("
              "overduebookid INT AUTO_INCREMENT PRIMARY KEY,"
              "UserName VARCHAR(50),"
              "user_id INT,"
              "Rented_book VARCHAR(50), "
              "overdue_days INT,"
              "Fine_amount INT),"
              "FOREIGN KEY(user_id) REFERENCES Users(userid)")"""


# Register/account creation function

# create_tables()

def register():
    global userid
    while True:
        try:
            print("Register your details here. Please Ensure to give the role_id during registration as 1!!!")
            first_name = input("Enter the first name: ")
            if re.fullmatch(r"[A-Za-z]{2,25}", first_name):
                break
            else:
                print("INVALID! Enter only alphabets of length 2 to 25.")
        except Exception as e:
            print(f"Error: {e}")

    while True:
        try:

            last_name = input("Enter the last name: ")
            if re.fullmatch(r"[A-Za-z]{2,25}", last_name):
                break
            else:
                print("INVALID! Enter only alphabets of length 2 to 25.")
        except Exception as e:
            print(f"Error: {e}")

    while True:
        try:

            username = input("Enter the username: ")
            if re.fullmatch(r"[A-Za-z]{2,25}", username):
                break
            else:
                print("INVALID! Enter only alphabets of length 2 to 25.")
        except Exception as e:
            print(f"Error: {e}")

    while True:
        mobile_number = input("Enter the phone number: ")
        if re.fullmatch(r"[6789]\d{9}", mobile_number):
            break
        else:
            print("INVALID! Enter a valid 10-digit phone number.")

    while True:
        email_id = input("Enter the email id: ")
        if re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_id):
            break
        else:
            print("INVALID! Enter a valid email id.")

    while True:
        role_id = input("Enter the role id: ")
        if re.fullmatch(r'1', role_id):
            break
        else:
            print("INVALID! Enter a valid role id.")

    while True:
        userid = input("Create a user id: ")
        if " " not in userid and re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,16}$', userid):

            break
        else:
            print("INVALID! Should be an alphanumeric character of length 6 to 16 without spaces.")

    while True:
        password = input("Enter the password: ")
        if " " not in password and re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+!_]).{6,16}$', password):

            break
        else:
            print("""INVALID! Password should contain:
            - At least one capital letter
            - At least one small letter
            - At least one number
            - At least one special character [ @ # $ % ^ & + ! _ ]
            - Length between 6 and 16 characters""")

    try:
        insert_query = """
            INSERT INTO users(userid,first_name,last_name,mobile_number,email_id,username,password,role_id) 
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
        """
        login.execute(insert_query,
                      (userid, first_name, last_name, mobile_number, email_id, username, password, role_id))
        databaseobj.commit()
        print("You have successfully registered!")
        user_page(userid)
    except mysql.connector.IntegrityError:
        print("User ID already exists")


# after  successfull registration, it should be directed to userhome page

def user_page(userid):
    print("Welcome to the User Page!")
    while True:
        print("""-------------------------------
              WELCOME TO USER PAGE 
              -------------------------------
              -> Choose an option:
              1. View list of all Books
              2. Membership Plans Available
              3. Search by Author
              4. Search by Genre
              5. Search by Title
              6. Rent a Book
              7. Logout""")
        number = input("Enter a number from the above list: ")
        if number == "1":
            Viewlistofall()
        elif number == "2":
            MembershipPlans()
        elif number == "3":
            searchbyAuthor()
        elif number == "4":
            searchbygenre()
        elif number == "5":
            SearchbyTitle()
        elif number == "6":
            Rentabook()
        elif number == "7":
            print("!!THANKS FOR ENGAGING WITH OUR APP!!")
            break
        else:
            print("Invalid choice, enter a number from 1 to 6.")



# user viewing list of books
def Viewlistofall():
    query = 'SELECT book_id, book_title, published_year FROM Books ORDER BY book_title ASC'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["book_id", "book_title",  "published_year"]))
    else:
        print("The list is empty.")


def MembershipPlans():
    while True:
        print("""                       
        -> Choose a membership plan to continue:
        1. Monthly Plan
        2. Annual Plan

        """)
        choice = input("Enter your choice from the above list: ")

        if choice in ["1", "2"]:
            membership_plan = "Monthly Plan" if choice == "1" else "Annual Plan"
            print(f"You have selected the {membership_plan}.")

            # Input membership details
            while True:
                try:
                    start_date = input("Enter the start date (YYYY-MM-DD): ")
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("INVALID! Enter the date in YYYY-MM-DD format.")

            while True:
                try:
                    end_date = input("Enter the end date (YYYY-MM-DD): ")
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    if end_date <= start_date:
                        print("INVALID! End date should be after the start date.")
                    else:
                        break
                except ValueError:
                    print("INVALID! Enter the date in YYYY-MM-DD format.")

            user_id = input("Enter your user ID: ")

            # Insert the membership details into the database
            membership(user_id, membership_plan, start_date, end_date)

            print(f"Successfully obtained the {membership_plan}.")
            print("The amount is Successfully cards")
            break
        else:
            print("Invalid choice! Enter 1 or 2 only.")


def membership(user_id, membership_plan, start_date, end_date):
    try:
        # Fetch the next membership ID
        query = "SELECT MAX(mem_id) FROM Membership"
        login.execute(query)
        result = login.fetchone()
        mem_id = (result[0] or 0) + 1

        insert_query = """
            INSERT INTO Membership (mem_id, membership_plan, start_date, end_date, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        login.execute(insert_query, (mem_id, membership_plan, start_date, end_date, user_id))
        databaseobj.commit()

        print("Membership details have been successfully recorded.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

# Function to search for a book by author
def searchbyAuthor():
    author_name = input("Enter the author name you want to search for: ")

    # Update query to search by author's name
    search_query = """
        SELECT b.book_id, b.book_title
        FROM Books b
        JOIN author a ON b.author_id = a.author_id
        WHERE a.author_name = %s
    """
    login.execute(search_query, (author_name,))
    books = login.fetchall()

    if books:
        print(f"Books found by author '{author_name}':")
        for book in books:
            print(f"- {book[1]}")
        return [book[0] for book in books], [book[1] for book in books]
    else:
        print("No books found by the specified author.")
        return None, None

# Function to search for books by genre
def searchbygenre():
    # Fetch available genres from the genre table
    genre_query = "SELECT genre_name FROM genre"
    login.execute(genre_query)
    genres = login.fetchall()

    if genres:
        print("Available Genres:")
        for genre in genres:
            print(f"- {genre[0]}")

        genre_name = input("Enter the genre name: ").strip()

        # Validate the selected genre
        if genre_name in [g[0] for g in genres]:
            # Search for books by genre name
            search_query = """
                SELECT b.book_id, b.book_title FROM Books b 
                JOIN genre g ON b.genre_id = g.genre_id 
                WHERE g.genre_name=%s
            """
            login.execute(search_query, (genre_name,))
            books = login.fetchall()

            if books:
                print(f"Books available in the {genre_name} genre:")
                for idx, book in enumerate(books, start=1):
                    print(f"{idx}. {book[1]}")

                book_index = int(input("Enter the number of the book you want to select: ")) - 1
                print("The book is selected")
                if 0 <= book_index < len(books):
                    return books[book_index][0], books[book_index][1]
                else:
                    print("Invalid selection. Please try again.")
                    return None, None
            else:
                print(f"No books found in the {genre_name} genre.")
                return None, None
        else:
            print("Invalid genre name. Please try again.")
            return None, None
    else:
        print("No genres available. Please check the genre table.")
        return None, None

def SearchbyTitle():
    book_title = input("Enter the book title you want to search for: ")

    # Update query to search by book's title and retrieve additional details
    search_query = """
        SELECT b.book_id, b.book_title, b.published_year, a.author_name
        FROM Books b
        JOIN author a ON b.author_id = a.author_id
        WHERE b.book_title = %s
    """
    try:
        login.execute(search_query, (book_title,))
        books = login.fetchall()

        if books:
            print(f"Books found with title '{book_title}':")
            for book in books:
                print(f"Book ID: {book[0]}")
                print(f"Book Title: {book[1]}")
                print(f"Published Year: {book[2]}")
                print(f"Author: {book[3]}")
                print("-" * 30)  # Separator for better readability
            return books
        else:
            print("No books found with the specified title.")
            return None
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

# Function to rent a book, with options to search by title or genre
def Rentabook():
    # Prompt for book selection
    print("Enjoy our special launch offer: Rent a book for just $15 and keep it for up to 15 days.")
    book_id = input("Enter the book ID you want to rent: ")

    # Validate book_id input
    if not re.fullmatch(r'\d+', book_id):
        print("INVALID! Enter a numeric book ID.")
        return

    book_id = int(book_id)

    # Fetch book details
    book_query = "SELECT book_title FROM Books WHERE book_id = %s"
    login.execute(book_query, (book_id,))
    book = login.fetchone()

    if not book:
        print("No book found with the provided ID.")
        return

    book_title = book[0]

    # Set the rent start date to the current date
    rent_start_date = date.today()

    # Collect rental end date and validate it
    while True:
        try:
            rent_end_date = input("Enter the rent end date (YYYY-MM-DD): ")
            rent_end_date = datetime.strptime(rent_end_date, "%Y-%m-%d").date()

            # Ensure the end date is within 10 days of the start date
            max_end_date = rent_start_date + timedelta(days=10)
            if rent_end_date > max_end_date:
                print(f"INVALID! The end date must be within 10 days of the start date ({max_end_date}).")
            elif rent_end_date < rent_start_date:
                print("INVALID! Rent end date must be after the start date.")
            else:
                break
        except ValueError:
            print("INVALID! Enter the date in YYYY-MM-DD format.")

    # Collect payment details
    payment_method = input("Enter payment method (e.g., credit card, PayPal): ")
    user_id = input("Enter your user ID: ")

    # Insert payment details
    try:
        payment_query = "INSERT INTO Payment (payment_method, user_id) VALUES (%s, %s)"
        login.execute(payment_query, (payment_method, user_id))
        databaseobj.commit()

        # Fetch the generated payment_id
        payment_id = login.lastrowid

        # Insert rental details
        rent_amount = 15  # Assuming a fixed rent amount as mentioned
        rent_query = """
            INSERT INTO Rent (rent_amount, rent_start_date, rent_end_date, user_id, book_id, payment_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        login.execute(rent_query, (rent_amount, rent_start_date, rent_end_date, user_id, book_id, payment_id))
        databaseobj.commit()

        print("Successfully rented your book!")

        # Display the rented book information
        rented_info_query = """
            SELECT rent_id, rent_amount, rent_start_date, rent_end_date, user_id, book_id
            FROM Rent
            WHERE rent_id = %s
        """
        login.execute(rented_info_query, (login.lastrowid,))
        rented_info = login.fetchone()

        if rented_info:
            print(tabulate([rented_info],
                           headers=["rent_id", "rent_amount", "rent_start_date", "rent_end_date", "user_id", "book_id"]))
        else:
            print("Failed to retrieve rented information.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")


                                #-------------------ADMIN PAGE--------------------#
def admin_page():
    print("!Welcome to the Admin Page!")
    while True:
        print("""-------------------------------
              WELCOME TO ADMIN PAGE 
              -------------------------------
              -> Choose an option:
              1. Add Books
              2. View Application
              3. List of User
              4. View Book
              5. View Overdue Book
              6. Delete Book
              7. Listofrentbook
              8. Logout""")
        number = input("Enter a number from the above list: ")
        if number == "1":
            AddBooks()
        elif number == "2":
            ViewApplication()
        elif number == "3":
            ListofUser()
        elif number == "4":
            ViewBook()
        elif number == "5":
            ViewOverdueBook()
        elif number == "6":
            DeleteBook()
        elif number == "7":
            Listofrentbook()
        elif number == "8":
            print("!!THANKS FOR ENGAGING WITH OUR APP!!")
            break
        else:
            print("Invalid choice, enter a number from 1 to 6.")

def AddBooks():
    while True:
        book_title = input("Enter the book name: ").title()
        if re.match("^[A-Za-z\s]+$", book_title):
            break
        else:
            print("Wrong Attempt! Use only alphabets")

    while True:
        author_name = input("Enter the author name: ").title()
        if re.match("^[A-Za-z\s]+$", author_name):
            # Check if the author already exists
            check_author_query = "SELECT author_id FROM author WHERE author_name = %s"
            login.execute(check_author_query, (author_name,))
            author = login.fetchone()
            if author:
                author_id = author[0]
                print(f"Author '{author_name}' already exists.")
            else:
                # Insert the new author into the author table
                insert_author_query = "INSERT INTO author (author_name) VALUES (%s)"
                login.execute(insert_author_query, (author_name,))
                databaseobj.commit()
                author_id = login.lastrowid
                print(f"Author '{author_name}' added successfully.")
            break
        else:
            print("Wrong Attempt! Use only alphabets")

    while True:
        genre_name = input("Enter the genre: ").title()
        if re.match("^[A-Za-z\s]+$", genre_name):
            # Check if the genre already exists
            check_genre_query = "SELECT genre_id FROM genre WHERE genre_name = %s"
            login.execute(check_genre_query, (genre_name,))
            genre = login.fetchone()
            if genre:
                genre_id = genre[0]
                print(f"Genre '{genre_name}' already exists.")
            else:
                # Insert the new genre into the genre table
                insert_genre_query = "INSERT INTO genre (genre_name) VALUES (%s)"
                login.execute(insert_genre_query, (genre_name,))
                databaseobj.commit()
                genre_id = login.lastrowid
                print(f"Genre '{genre_name}' added successfully.")
            break
        else:
            print("Wrong Attempt! Use only alphabets")

    while True:
            published_year = input("Enter the published year (YYYY): ")
            if published_year.isdigit() and len(published_year) == 4 and 1900 <= int(published_year) <= 2155:
                break
            else:
                print("Invalid year. Please enter a valid year between 1900 and 2155.")

    while True:
        try:
            price = int(input("Enter the price: "))
            break
        except ValueError:
            print("INVALID! Use only alphabets and spaces for the price ")

    # Insert the book details into the Books table
    insert_book_query = "INSERT INTO Books (book_title, author_id, genre_id, published_year,price) VALUES (%s, %s, %s, %s, %s)"
    login.execute(insert_book_query, (book_title, author_id, genre_id, published_year, price))
    databaseobj.commit()

    print(f"Book '{book_title}' added successfully!")

def ViewApplication():
    query = "Select * from Users"
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["user_id", "firstname", "lastname","email_id","mobile_number","username","password","role_id"]))
    else:
        print("The application list is empty.")

def ListofUser():
    query = "Select * from listofusers"
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Uid","UNAME","Currentpassword","Membershipid,Plan_currently","Pending_dues"]))
    else:
        print("The application list is empty.")

def ViewBook():
    query = "Select * from books"
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["book_id", "book_title", "published_year", "author_id", "genre_id","price"]))
    else:
        print("The application list is empty.")

def ViewOverdueBook():
    query = "Select * from overduebooks"
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["overduebookid", "UserName", "user_id","Rented_book", "overdue_days", "Fine_amount"]))
    else:
        print("The overduebooks list is empty.")

def DeleteBook():
    while True:
        try:
            # Prompt admin for the book ID to delete
            book_id = input("Enter the book ID you want to delete: ")

            # Validate the book ID input
            if not re.fullmatch(r'\d+', book_id):
                print("INVALID! Enter a numeric book ID.")
                continue

            book_id = int(book_id)

            # Check if the book exists in the Books table
            check_query = "SELECT book_title FROM Books WHERE book_id = %s"
            login.execute(check_query, (book_id,))
            book = login.fetchone()

            if book:
                # If the book exists, delete it
                delete_query = "DELETE FROM Books WHERE book_id = %s"
                login.execute(delete_query, (book_id,))
                databaseobj.commit()
                print(f"The book '{book[0]}' with ID {book_id} has been successfully deleted.")
            else:
                print(f"No book found with ID {book_id}.")
            break

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"Error: {e}")

# LOGIN page for entering into the app, it can be Admin or Users........
def loginfun():
    while True:
        try:
            userid = input("Enter your user ID: ")
            password = input("Enter your password: ")

            # Query to check user credentials
            query = """
            SELECT u.userid, u.password, r.role_name
            FROM Users u
            JOIN role r ON u.role_id = r.role_id
            WHERE u.userid = %s AND u.password = %s
            """
            login.execute(query, (userid, password))
            result = login.fetchone()

            if result:
                # If the user exists and password matches
                role_name = result[0]
                if role_name == 'admin':
                    admin_page()
                else:
                    user_page(userid)
                break
            else:
                print("Invalid user ID or password. Please try again.")

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"Error: {e}")

def Listofrentbook():
    query = "Select * from rent"
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["rent_id", "rentname", "rent_start_date","rent_end_date","user_id","book_id","payment_id"]))
    else:
        print("The application list is empty.")


# Main menu / HOME PAGE..........

while True:
    print("""
          WELCOME TO EAZ TO READ Library 
          -------------------------------
          -> Choose an option:
          1. Login
          2. New User/ SignUp Here
          3. Exit""")
    number = input("Enter a number from the above list: ")
    if number == "1":
        loginfun()
    elif number == "2":
        register()
    elif number == "3":
        print(" -----------!Thanks for engaging with our app! You're amazing!----------")
        break
    else:
        print("Invalid choice, enter a number from 1 to 3.")