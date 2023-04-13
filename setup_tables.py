import mysql.connector
import random

# Set up the MySQL connection
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="bpanny",
        password="software",
        database="phs"
    )
    return connection

# Create patient events table in phs database
def create_table_if_not_exists(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pt_id INT NOT NULL,
        message VARCHAR(255) NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (pt_id) REFERENCES patients(pt_id)
    )
    """)
    connection.commit()

# CREATE TABLE phs.patients (id_number INT PRIMARY KEY);
def create_patient_table_if_not_exists(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        pt_id INT PRIMARY KEY,
        pt_first_name VARCHAR(255) NOT NULL,
        pt_last_name VARCHAR(255) NOT NULL,
        pt_location VARCHAR(255) NOT NULL,
        pt_phone VARCHAR(20) NOT NULL
    )
    """)
    connection.commit()

# CREATE TABLE phs.interactions (id_number INT PRIMARY KEY);
def create_staff_table_if_not_exists(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        staff_id INT PRIMARY KEY,
        staff_first_name VARCHAR(255) NOT NULL,
        staff_last_name VARCHAR(255) NOT NULL,
        staff_location VARCHAR(255) NOT NULL,
        staff_email VARCHAR(255) NOT NULL,
        staff_phone VARCHAR(20) NOT NULL
    )
    """)
    connection.commit()

def create_interaction_table_if_not_exists(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_ID INT AUTO_INCREMENT PRIMARY KEY,
        pt_id INT NOT NULL,
        staff_id INT NOT NULL,
        staff_notes TEXT NOT NULL,
        FOREIGN KEY (pt_id) REFERENCES patients(pt_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    )
    """)
    connection.commit()

def create_emergency_log_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_log (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        pt_id INT NOT NULL,
        staff_id INT NOT NULL,
        message_count INT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (pt_id) REFERENCES patients(pt_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    )
    """)
    connection.commit()

def create_past_emergency_log_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS past_emergency_log (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        pt_id INT NOT NULL,
        staff_id INT NOT NULL,
        message_count INT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (pt_id) REFERENCES patients(pt_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    )
    """)
    connection.commit()


def insert_fake_patient(connection):
    fake_first_name = "John"
    fake_last_name = "Doe"
    fake_location = "15213"
    fake_phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO patients (pt_id, pt_first_name, pt_last_name, pt_location, pt_phone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (1, fake_first_name, fake_last_name, fake_location, fake_phone)
    )
    connection.commit()
    
def insert_fake_staff(connection):
    fake_first_name = "Jane"
    fake_last_name = "Doe"
    fake_location = "15213"
    fake_email = "benjaminpanny@gmail.com"
    fake_phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO staff (staff_id, staff_first_name, staff_last_name, staff_location, staff_email, staff_phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (1, fake_first_name, fake_last_name, fake_location, fake_email, fake_phone)
    )
    connection.commit()

def drop_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        DROP TABLE IF EXISTS events, interactions, patients, staff, emergency_log, past_emergency_log
        """
    )
    connection.commit()

# Set up the MySQL connection
connection = connect_to_db()

# Insert a single fake patient into the database

drop_all_tables(connection)
create_staff_table_if_not_exists(connection)
create_patient_table_if_not_exists(connection)
create_table_if_not_exists(connection)
create_interaction_table_if_not_exists(connection)
create_emergency_log_table(connection)
create_past_emergency_log_table(connection)
insert_fake_patient(connection)
insert_fake_staff(connection)

# Close the connection
connection.close()