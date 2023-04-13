import mysql.connector
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from uploader import connect_to_db


def get_patient_location(pt_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT pt_location FROM patients WHERE pt_id = %s", (pt_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def get_assigned_staff(pt_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT staff_id FROM emergency_log WHERE pt_id = %s", (pt_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def get_available_staff_locations():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT staff_id, staff_location FROM staff WHERE staff_id NOT IN (SELECT staff_id FROM emergency_log)")
    result = cursor.fetchall()
    connection.close()
    return result

def send_message_to_closest_staff(pt_id, pt_location, available_staff_locations):
    closest_staff_id = None
    closest_distance = float("inf")
    for staff_id, staff_location in available_staff_locations:
        distance = abs(int(pt_location) - int(staff_location))
        if distance < closest_distance:
            closest_distance = distance
            closest_staff_id = staff_id

    # Sending a message (replace with actual implementation)
    print(f"Sending message to staff {closest_staff_id}")

    return closest_staff_id

def get_emergency_info(pt_id):
    with ThreadPoolExecutor() as executor:
        pt_location_future = executor.submit(get_patient_location, pt_id)
        assigned_staff_future = executor.submit(get_assigned_staff, pt_id)
        available_staff_locations_future = executor.submit(get_available_staff_locations)

        pt_location = pt_location_future.result()
        assigned_staff = assigned_staff_future.result()
        available_staff_locations = available_staff_locations_future.result()

    return pt_location, assigned_staff, available_staff_locations

def log_emergency_status(pt_id, staff_id, message_count):
    connection = connect_to_db()
    cursor = connection.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO emergency_log (pt_id, staff_id, message_count, timestamp)
        VALUES (%s, %s, %s, %s)
        """,
        (pt_id, staff_id, message_count, timestamp)
    )
    connection.commit()
    connection.close()


def emergency_manager(pt_id):
    pt_location, assigned_staff, available_staff_locations = get_emergency_info(pt_id)

    if assigned_staff:
        # Send a message to the assigned staff (replace with actual implementation)
        print(f"Sending message to assigned staff {assigned_staff}")
        staff_id = assigned_staff
    else:
        staff_id = send_message_to_closest_staff(pt_id, pt_location, available_staff_locations)

    # Log the emergency status as "open"
    log_emergency_status(pt_id, staff_id, 1)

    # Later, when the emergency is resolved, update the status and message count accordingly
    # log_emergency_status(pt_id, staff_id, message_count, "resolved")
