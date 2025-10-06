import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- Database Connection Details (UPDATE THESE) ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12341234"
DB_NAME = "little_lemon"

# --- Path to your Excel file ---
EXCEL_FILE_PATH = "LittleLemon_data(Orders).xlsx"


def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, database=DB_NAME, port=3307
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def load_data_from_excel(file_path):
    """Extract data from Excel, transform it, and load it into the database."""
    try:
        df = pd.read_excel(file_path)
        print("Excel file read successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # --- 1. TRANSFORM DATA ---

    # Clean up column names to be database-friendly (no spaces, consistent casing)
    df.columns = df.columns.str.replace(" ", "")

    # Create a DataFrame for Customers, dropping duplicates to get unique customers
    customers_df = df[
        ["CustomerID", "CustomerName", "City", "Country", "PostalCode", "CountryCode"]
    ].drop_duplicates(subset=["CustomerID"])

    # Create a DataFrame for MenuItems, dropping duplicates
    # Note: We are assuming a combination of these fields defines a unique menu item
    menu_items_df = df[
        [
            "CourseName",
            "CuisineName",
            "StarterName",
            "DesertName",
            "Drink",
            "Sides",
            "Cost",
            "Sales",
        ]
    ].drop_duplicates()
    # Rename 'Sales' to 'SalesPrice' to match the database schema
    menu_items_df = menu_items_df.rename(columns={"Sales": "SalesPrice"})

    # Create a DataFrame for Orders
    # Note: Renaming 'Sales' to 'TotalCost' to match the database schema
    orders_df = df[
        [
            "OrderID",
            "OrderDate",
            "DeliveryDate",
            "Quantity",
            "Sales",
            "Discount",
            "DeliveryCost",
            "CustomerID",
        ]
    ]
    orders_df = orders_df.rename(columns={"Sales": "TotalCost"})

    customers_df = customers_df.astype(object).where(pd.notnull(customers_df), None)
    menu_items_df = menu_items_df.astype(object).where(pd.notnull(menu_items_df), None)
    orders_df = orders_df.astype(object).where(pd.notnull(orders_df), None)
    print("Cleaned NaN values for SQL insertion.")

    # --- 2. LOAD DATA ---
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        # Load Customers
        print("\nLoading Customers...")
        customer_sql = """
        INSERT IGNORE INTO Customers (CustomerID, CustomerName, City, Country, PostalCode, CountryCode) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        for index, row in customers_df.iterrows():
            cursor.execute(customer_sql, tuple(row))
        print(f"{cursor.rowcount} new customers loaded.")

        # Load MenuItems
        print("\nLoading Menu Items...")
        menu_item_sql = """
        INSERT INTO MenuItems (CourseName, CuisineName, StarterName, DesertName, Drink, Sides, Cost, SalesPrice) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # We need to handle potential duplicates manually here if we don't have a unique constraint
        # For simplicity, we assume we're loading into an empty table.
        # If running multiple times, consider adding a UNIQUE constraint in SQL.
        for index, row in menu_items_df.iterrows():
            cursor.execute(menu_item_sql, tuple(row))
        print(f"{cursor.rowcount} menu items loaded.")

        # Load Orders
        print("\nLoading Orders...")
        order_sql = """
        INSERT IGNORE INTO Orders (OrderID, OrderDate, DeliveryDate, Quantity, TotalCost, Discount, DeliveryCost, CustomerID) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for index, row in orders_df.iterrows():
            cursor.execute(order_sql, tuple(row))
        print(f"{cursor.rowcount} new orders loaded.")

        # Commit the changes to the database
        conn.commit()
        print("\nAll data has been successfully loaded and committed to the database.")

    except Error as e:
        print(f"Error during data loading: {e}")
        conn.rollback()  # Roll back any changes if an error occurs
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")


# --- Run the ETL process ---
if __name__ == "__main__":
    load_data_from_excel(EXCEL_FILE_PATH)
