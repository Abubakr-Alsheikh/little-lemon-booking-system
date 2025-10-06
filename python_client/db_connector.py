import mysql.connector
from mysql.connector import Error

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12341234"
DB_NAME = "little_lemon"


# --- Database Connection ---
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=3307,
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# Establish connection (replace with your details)
conn = create_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
cursor = conn.cursor()

# --- Stored Procedure Creation and Execution ---
# The assignment asks you to "create a procedure using Python".
# This means you write the SQL for the procedure and execute it from your Python script.

# Drop procedures if they exist to allow for re-running the script
cursor.execute("DROP PROCEDURE IF EXISTS GetMaxQuantity")
cursor.execute("DROP PROCEDURE IF EXISTS ManageBooking")
cursor.execute("DROP PROCEDURE IF EXISTS UpdateBooking")
cursor.execute("DROP PROCEDURE IF EXISTS AddBooking")
cursor.execute("DROP PROCEDURE IF EXISTS CancelBooking")

get_max_quantity_sql = """
CREATE PROCEDURE GetMaxQuantity()
BEGIN
    SELECT MAX(Quantity) AS `Max Quantity` FROM Orders;
END
"""
cursor.execute(get_max_quantity_sql)
print("Procedure GetMaxQuantity created.")

# How to call it:
# cursor.callproc('GetMaxQuantity')
# for result in cursor.stored_results():
#     print(result.fetchone())

manage_booking_sql = """
CREATE PROCEDURE ManageBooking(IN check_date DATE, IN table_num INT)
BEGIN
    SELECT 
        CASE 
            WHEN EXISTS (SELECT 1 FROM Bookings WHERE BookingDate = check_date AND TableNumber = table_num) 
            THEN CONCAT('Table ', table_num, ' is already booked')
            ELSE CONCAT('Table ', table_num, ' is available')
        END AS `Booking Status`;
END
"""
cursor.execute(manage_booking_sql)
print("Procedure ManageBooking created.")

# How to call it:
# cursor.callproc('ManageBooking', ['2023-11-15', 3])
# for result in cursor.stored_results():
#     print(result.fetchone())

add_booking_sql = """
CREATE PROCEDURE AddBooking(IN booking_id INT, IN customer_id INT, IN table_num INT, IN booking_date DATE)
BEGIN
    INSERT INTO Bookings (BookingID, CustomerID, TableNumber, BookingDate)
    VALUES (booking_id, customer_id, table_num, booking_date);
    SELECT "New booking added" AS "Confirmation";
END
"""
cursor.execute(add_booking_sql)
print("Procedure AddBooking created.")

# How to call it:
# cursor.callproc('AddBooking', [10, 3, 4, '2023-12-10'])
# conn.commit()

update_booking_sql = """
CREATE PROCEDURE UpdateBooking(IN booking_id INT, IN new_booking_date DATE)
BEGIN
    UPDATE Bookings SET BookingDate = new_booking_date WHERE BookingID = booking_id;
    SELECT CONCAT("Booking ", booking_id, " updated") AS "Confirmation";
END
"""
cursor.execute(update_booking_sql)
print("Procedure UpdateBooking created.")

# How to call it:
# cursor.callproc('UpdateBooking', [10, '2023-12-12'])
# conn.commit()
