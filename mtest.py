import mysql.connector
from tabulate import tabulate
from datetime import date, timedelta
import re

# Database connection setup
databaseobj = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ragul',
    database='hotelroombookings'
)
login = databaseobj.cursor()

# Create tables
# Creating table details in database Hotelroombookings
login.execute("""
    CREATE TABLE IF NOT EXISTS details (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        mobile_number VARCHAR(15),
        email_id VARCHAR(50),
        username VARCHAR(50) UNIQUE,
        password VARCHAR(50),
        role VARCHAR(50)
    )
""")
# Creating table Rooms in database Hotelroombookings
login.execute("""
    CREATE TABLE IF NOT EXISTS Rooms (
        Room_id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50),
        price_per_day_with_tax INT,
        status VARCHAR(50)
    )
""")
# Creating table PreBooking in database Hotelroombookings
login.execute("""
    CREATE TABLE IF NOT EXISTS PreBooking (
        booking_id VARCHAR(50) PRIMARY KEY,
        customer_name VARCHAR(50),
        room_id INT,
        date_of_booking DATE,
        date_of_occupancy DATE,
        number_of_days INT,
        advance_received INT
    )
""")
# Creating table Customer in database Hotelroombookings
login.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        booking_id VARCHAR(50),
        room_id INT,
        contact_number VARCHAR(15),
        address VARCHAR(50),
        FOREIGN KEY(booking_id) REFERENCES PreBooking(booking_id),
        FOREIGN KEY(room_id) REFERENCES Rooms(room_id)
    )
""")
# Creating table LoginInfoTable in database Hotelroombookings
login.execute("""
    CREATE TABLE IF NOT EXISTS LoginInfoTable (
        userid VARCHAR(50) PRIMARY KEY,
        password VARCHAR(50)
    )
""")

def category_list():
    select_query = "SELECT Room_id, category, price_per_day_with_tax FROM Rooms"
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room_id", "Category", "Price_per_day_with_tax"], tablefmt="psql"))
    else:
        print("No list found")

def occupied_room_list():
    today = date.today()
    query = '''
        SELECT r.Room_id, r.category, pb.date_of_occupancy, pb.customer_name
        FROM Rooms r
        JOIN PreBooking pb ON r.Room_id = pb.room_id
        WHERE pb.date_of_occupancy BETWEEN %s AND %s AND r.status = "Occupied"
    '''
    login.execute(query, (today, today + timedelta(days=2)))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room_id", "Category", "Date_of_occupancy", "Customer_name"], tablefmt="psql"))
    else:
        print("No rooms are occupied in the next two days.")

def list_of_rooms_pricewise():
    select_query = "SELECT Room_id, category, price_per_day_with_tax FROM Rooms ORDER BY price_per_day_with_tax ASC"
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room_id", "Category", "Price_per_day_with_tax"], tablefmt="psql"))
    else:
        print("No list found")

def search_by_booking_id():
    while True:
        booking_id = input("Enter the booking ID to search (e.g., BI123): ")
        if re.fullmatch(r"^[A-Z]{2}\d{3}$", booking_id):
            break
        else:
            print("Invalid Booking ID format! It should consist of 2 letters followed by 3 digits (e.g., AB123).")

    select_query = """
        SELECT pb.booking_id, pb.customer_name, pb.room_id, pb.date_of_booking, pb.date_of_occupancy, pb.number_of_days, pb.advance_received
        FROM PreBooking pb
        JOIN Customer c ON pb.booking_id = c.booking_id
        WHERE pb.booking_id = %s
    """
    login.execute(select_query, (booking_id,))
    result = login.fetchall()
    if result:
        print(tabulate(result,
                       headers=["Booking Id", "Customer Name", "Room Id", "Date of Booking", "Date of Occupancy",
                                "Number of Days", "Advance Received"], tablefmt="psql"))
    else:
        print("No details found for the given Booking ID.")

def unoccupied_rooms():
    select_query = "SELECT Room_id, category, price_per_day_with_tax, status FROM Rooms WHERE status = 'Unoccupied'"
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room ID", "Category", "Price Per Day", "Status"], tablefmt="psql"))
    else:
        print("No rooms are available")

def update_rooms():
    while True:
        room_id = input("Enter the Room ID to update to 'Unoccupied': ")
        if room_id.isdigit():
            break
        else:
            print("Use only numbers")

    select_query = "SELECT status FROM Rooms WHERE Room_id = %s"
    login.execute(select_query, (room_id,))
    result = login.fetchone()

    if result:
        current_status = result[0]
        if current_status == "Occupied":
            update_query = "UPDATE Rooms SET status = 'Unoccupied' WHERE Room_id = %s"
            login.execute(update_query, (room_id,))
            databaseobj.commit()
            print(f"Room ID {room_id} has been updated to 'occupied'.")
        else:
            print(f"Room ID {room_id} is already unoccupied.")
    else:
        print(f"No room found with ID {room_id}.")

def store_and_display_file():
    login.execute("SELECT * FROM Rooms")
    rooms = login.fetchall()
    with open('rooms_records.txt', 'w') as file:
        file.write(tabulate(rooms, headers=['Room ID', 'Category', 'Price per Day', 'Status'], tablefmt='psql'))
    print("Records have been written to rooms_records.txt")
    with open('rooms_records.txt', 'r') as file:
        print(file.read())

def list_available_rooms():
    select_query = "SELECT Room_id, category, price_per_day_with_tax, status FROM Rooms WHERE status = 'Occupied'"
    login.execute(select_query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["Room ID", "Category", "Price Per Day", "Status"], tablefmt="psql"))
    else:
        print("No rooms are available")

def book_a_room():
    try:
        # Display available rooms
        unoccupied_rooms()

        # Prompt the user for room selection
        while True:
            room_id = input("Enter the Room ID you want to book: ")
            if room_id.isdigit():
                room_id = int(room_id)
                login.execute("SELECT status FROM Rooms WHERE Room_id = %s", (room_id,))
                room_status = login.fetchone()

                if room_status and room_status[0] == "Unoccupied":
                    break
                else:
                    print("The room is either occupied or does not exist. Please choose another room.")
            else:
                print("Please enter a valid Room ID (numbers only).")

        customer_name = input("Enter customer name: ")
        date_of_booking = date.today()

        while True:
            try:
                date_of_occupancy = input("Enter the date of occupancy (YYYY-MM-DD): ")
                date_of_occupancy = datetime.strptime(date_of_occupancy, "%Y-%m-%d").date()
                if date_of_occupancy >= date_of_booking:
                    break
                else:
                    print("Date of occupancy cannot be before the date of booking.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        while True:
            try:
                number_of_days = int(input("Enter the number of days the customer will occupy the room: "))
                if number_of_days > 0:
                    break
                else:
                    print("Number of days must be positive.")
            except ValueError:
                print("Please enter a valid number of days.")

        while True:
            try:
                advance_received = int(input("Enter the advance payment received: "))
                if advance_received >= 0:
                    break
                else:
                    print("Advance payment cannot be negative.")
            except ValueError:
                print("Please enter a valid amount.")

        booking_id = f"BI{room_id}{int(datetime.now().timestamp())}"

        prebooking_query = """
            INSERT INTO PreBooking (booking_id, customer_name, room_id, date_of_booking, date_of_occupancy, number_of_days, advance_received)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        login.execute(prebooking_query, (booking_id, customer_name, room_id, date_of_booking, date_of_occupancy, number_of_days, advance_received))

        customer_contact = input("Enter the customer's contact number: ")
        customer_address = input("Enter the customer's address: ")

        customer_query = """
            INSERT INTO Customer (booking_id, room_id, contact_number, address)
            VALUES (%s, %s, %s, %s)
        """
        login.execute(customer_query, (booking_id, room_id, customer_contact, customer_address))

        update_room_query = "UPDATE Rooms SET status = 'Occupied' WHERE Room_id = %s"
        login.execute(update_room_query, (room_id,))

        databaseobj.commit()

        print(f"Room ID {room_id} has been successfully booked under Booking ID {booking_id}.")

    except Exception as e:
        print("An error occurred during the booking process:", e)

def menu():
    while True:
        print("""                -------------------------------
                                    WELCOME TO ADMIN 
                                 -------------------------------
                                -> Choose an option:
                                1. Display Category wise list of rooms and their Rate per day
                                2. List of all rooms which are occupied for next two days
                                3. Display list of all rooms in increasing order of rate per day
                                4. Search Rooms based on BookingID and display customer details
                                5. Display rooms which are not booked
                                6. Update room status to unoccupied
                                7. Store all records in a file and display from file
                                8. Exit""")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            category_list()
        elif choice == '2':
            occupied_room_list()
        elif choice == '3':
            list_of_rooms_pricewise()
        elif choice == '4':
            search_by_booking_id()
        elif choice == '5':
            unoccupied_rooms()
        elif choice == '6':
            update_rooms()
        elif choice == '7':
            store_and_display_file()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

def loginfun():
    global userid
    while True:
        userid = input("Enter the user ID: ")
        if userid:
            break
        else:
            print("This field cannot be empty.")

    while True:
        password = input("Enter the password: ")
        if password:
            break
        else:
            print("This field cannot be empty.")

    select_query = """
    SELECT * FROM LoginInfoTable
    WHERE userid=%s COLLATE utf8mb4_bin AND password=%s COLLATE utf8mb4_bin
    """
    login.execute(select_query, (userid, password))
    result = login.fetchone()
    if result:
        print("Login successful!")
        menu()
    else:
        print("Incorrect user ID or password.")

if __name__ == "__main__":
    while True:
        print("""-------------------------------
              WELCOME TO Admin 
              -------------------------------
              -> Choose an option:
              1. Login
              2. Logout""")
        number = input("Enter a number from the above list: ")
        if number == "1":
            loginfun()
        elif number == "2":
            print("!!THANKS FOR ENGAGING WITH OUR APP!!")
            break
        else:
            print("Invalid choice, enter a number from 1 to 2.")
