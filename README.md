# Little Lemon Booking System - Database Engineer Capstone Project

This repository contains the final submission for the Database Engineer Capstone project. The objective was to design, implement, and analyze a database system for the fictional restaurant, "Little Lemon". This project demonstrates skills in data modeling, database creation (MySQL), procedural SQL, Python database integration, ETL processes, and data visualization.

**Technologies Used:** `MySQL`, `Python`, `Pandas`, `MySQL Connector`, `Metabase`, `Docker`

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Meeting the Grading Criteria](#meeting-the-grading-criteria)
3. [Database Design and Schema](#database-design-and-schema)
4. [Stored Procedures Implementation](#stored-procedures-implementation)
5. [ETL - Data Loading Process](#etl---data-loading-process)
6. [Data Analysis and Visualization with Metabase](#data-analysis-and-visualization-with-metabase)
7. [Repository Structure](#repository-structure)
8. [How to Set Up and Run the Project](#how-to-set-up-and-run-the-project)

---

## Project Overview

The project involved several key stages:

1. **Database Design:** Normalizing a flat Excel file into a relational database schema to ensure data integrity and reduce redundancy.
2. **Database Implementation:** Creating the database and tables in MySQL using the generated schema.
3. **Backend Logic:** Developing a suite of stored procedures in SQL to manage booking data (add, update, cancel, etc.). These procedures were created and managed via a Python client.
4. **Data Ingestion:** Building a Python script to perform an ETL (Extract, Transform, Load) process, extracting data from the provided Excel file, transforming it for compatibility, and loading it into the newly designed database.
5. **Data Analysis:** Connecting the database to a business intelligence tool to create reports and an interactive dashboard for data analysis and insight generation.

## Meeting the Grading Criteria

This project successfully fulfills all the requirements outlined in the final assessment criteria:

- [x] **GitHub Repo Successfully Created:** The project is hosted in this public GitHub repository.
- [x] **Appropriate Project in Repo:** The repository contains all required artifacts for the Little Lemon database project.
- [x] **Appropriate ER Diagram:** An ER diagram is included, showing the normalized schema and table connections.
- [x] **`GetMaxQuantity()` Procedure Properly Implemented:** This procedure returns the maximum quantity from any order.
- [x] **`ManageBooking()` Procedure Properly Implemented:** This procedure checks the status of a table booking on a given date.
- [x] **`UpdateBooking()` Procedure Properly Implemented:** This procedure updates the date of an existing booking.
- [x] **`AddBooking()` Procedure Properly Implemented:** This procedure adds a new booking to the system.
- [x] **`CancelBooking()` Procedure Properly Implemented:** This procedure cancels and removes a booking from the system.

## Database Design and Schema

The initial dataset was a single flat file. To build a robust and scalable system, the data was normalized into four distinct tables. This separation reduces data redundancy and improves data integrity.

### ER Diagram

The relationships between the tables are visualized in the Entity-Relationship Diagram below:

![Little Lemon ER Diagram](https://raw.githubusercontent.com/Abubakr-Alsheikh/little-lemon-booking-system/main/diagrams/little_lemon_ERD.png)

### Tables

- **`Customers`**: Stores unique customer information.

- **`MenuItems`**: Stores information about each unique menu item.
- **`Orders`**: Contains high-level information about each order placed by a customer.
- **`Bookings`**: Manages table reservations, linking a customer to a specific table at a specific time.

The complete database model can be found in `sql/little_lemon_model.mwb`, and the creation script is in `sql/little_lemon_schema.sql`.

## Stored Procedures Implementation

All required stored procedures were written in SQL and deployed to the database using a Python script (`python_client/db_connector.py`). This demonstrates the ability to manage database objects programmatically.

- **`GetMaxQuantity()`**: Retrieves the highest quantity value found in the `Orders` table.
- **`ManageBooking(date, table_number)`**: Checks if a specific table is already booked on a given date and returns its status.
- **`AddBooking(booking_id, customer_id, table_number, date)`**: Inserts a new booking record into the `Bookings` table.
- **`UpdateBooking(booking_id, date)`**: Modifies the `BookingDate` for an existing booking.
- **`CancelBooking(booking_id)`**: Deletes a booking record from the `Bookings` table.

## ETL - Data Loading Process

A Python script, `load_data.py`, was created to handle the ETL process.

- **Extract:** It reads the raw data from the `LittleLemonData.xlsx` file using the `pandas` library.
- **Transform:** It cleans the column names, separates the flat data into distinct DataFrames matching the normalized schema (`Customers`, `MenuItems`, `Orders`), and critically, it handles empty cells by converting `NaN` values to `None` to ensure compatibility with SQL `NULL`.
- **Load:** It connects to the MySQL database and uses the `mysql-connector` library to efficiently load the transformed data into the respective tables using `executemany` for performance.

## Data Analysis and Visualization with Metabase

**Note on Visualization Tool:** This project utilizes **Metabase**, a powerful open-source business intelligence tool, as an alternative to Tableau. Metabase was chosen for its ease of setup via Docker, intuitive query builder, and powerful SQL integration, allowing for the rapid development of insightful reports and dashboards.

An interactive dashboard was created to analyze sales performance, customer behavior, and menu popularity.

### Final Sales Dashboard

![Little Lemon Metabase Dashboard](https://raw.githubusercontent.com/Abubakr-Alsheikh/little-lemon-booking-system/main/reports_metabase/metabase_final_dashboard.png)

The dashboard includes the following key reports:

1. **Sales Trend Over Time**: A line chart showing the total sales revenue per month, allowing stakeholders to identify trends and seasonality.
2. **Top 5 Customers by Sales**: A bar chart highlighting the most valuable customers, which can be used for targeted marketing efforts.
3. **Sales by Cuisine**: A pie chart breaking down sales by cuisine type, providing insights into the most popular menu categories.

## Repository Structure

```
/little-lemon-booking-system
│
├── README.md
├── diagrams/
│   └── little_lemon_ERD.png
│
├── python_client/
│   ├── db_connector.py        # Connects to DB and creates stored procedures
│   └── load_data.py           # ETL script to load data from Excel
│
├── reports_metabase/
│   ├── metabase_final_dashboard.png
│   ├── metabase_sales_by_cuisine.png
│   ├── metabase_sales_trend.png
│   └── metabase_top_customers.png
│
├── sql/
│   ├── little_lemon_model.mwb   # MySQL Workbench Model file
│   └── little_lemon_schema.sql  # SQL script to create database and tables
│
└── LittleLemonData.xlsx         # The original data file
```

## How to Set Up and Run the Project

Follow these steps to replicate the project environment.

### Prerequisites

- MySQL Server installed and running.

- Python 3.8+ installed.
- Docker Desktop installed and running.

### 1. Set Up the Database

1. Open MySQL Workbench or connect to your MySQL server via the command line.
2. Execute the entire `sql/little_lemon_schema.sql` script. This will create the `little_lemon` database, all necessary tables, and insert some sample data for testing.

### 2. Configure and Run Python Scripts

1. Navigate to the `python_client` directory.
2. Install required Python libraries:

    ```bash
    pip install pandas openpyxl mysql-connector-python
    ```

3. Open both `db_connector.py` and `load_data.py` and **update the database connection details** (host, username, password) at the top of each file.
4. Run the scripts from your terminal in the project's root directory:

    ```bash
    # This script creates the stored procedures
    python python_client/db_connector.py

    # This script loads the data from the Excel file
    python python_client/load_data.py
    ```

### 3. Launch and Configure Metabase

1. Run Metabase using Docker with the following command in your terminal:

    ```bash
    docker run -d -p 3000:3000 --name metabase metabase/metabase
    ```

2. Open your web browser and navigate to `http://localhost:3000`.
3. Complete the initial Metabase setup to create an admin account.
4. When prompted to add data, select "MySQL" and enter the following details:
    - **Host:** `host.docker.internal` (this allows the Docker container to connect to your local machine's MySQL instance).
    - **Database name:** `little_lemon`
    - **Username & Password:** Your MySQL credentials.
5. Metabase will now be connected to your database, and you can explore the data and build your own questions and dashboards.
