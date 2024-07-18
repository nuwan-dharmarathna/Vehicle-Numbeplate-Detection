import mysql.connector
from mysql.connector import Error, errorcode

import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    connection = None
    DB_NAME = "gate_system"
    
    try:
        connection = mysql.connector.connect(
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_HOST'),
            database = DB_NAME
        )
        if connection.is_connected():
            print(f"Connected to database '{DB_NAME}'")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    return connection

def create_database(connection, db_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database {db_name} already exists.")
        else:
            print(f"Failed creating database: {err}")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# connect to MySQL Server
connection = create_connection()

# create DB
create_database(connection, 'gate_system')

# SQL Queries to create tables
create_owner_table = """
CREATE TABLE owner (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    phone VARCHAR(10) NOT NULL
);
"""

create_vehicle_details_table = """
CREATE TABLE vehicle (
    vehicle_number VARCHAR(10) PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES owner(owner_id)
);
"""

create_vehicle_entries_table = """
CREATE TABLE vehicle_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(10),
    entry_time TIME NOT NULL,
    entry_date DATE NOT NULL,
    worker_id INT,
    FOREIGN KEY (vehicle_number) REFERENCES vehicle(vehicle_number),
    FOREIGN KEY (worker_id) REFERENCES owner(owner_id)
);
"""

# Execute the queries
execute_query(connection, create_owner_table)
execute_query(connection, create_vehicle_details_table)
execute_query(connection, create_vehicle_entries_table)






    
     