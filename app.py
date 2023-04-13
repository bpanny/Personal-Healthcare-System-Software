from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from uploader import connect_to_db


# Initialize Flask app
app = Flask(__name__)
app.secret_key = "software"

# Route and function for staff adding interaction
@app.route('/add_interaction', methods=['GET', 'POST'])
def add_interaction():
    if request.method == 'POST':
        pt_id = request.form['pt_id']
        staff_id = request.form['staff_id']
        staff_notes = request.form['staff_notes']

        # Establish a connection to the MySQL server
        connection = connect_to_db()

        cursor = connection.cursor()

        # Copy the emergency_log entry to past_emergency_log
        cursor.execute("""
            INSERT INTO past_emergency_log (pt_id, staff_id, message_count, timestamp)
            SELECT pt_id, staff_id, message_count, timestamp FROM emergency_log
            WHERE pt_id = %s AND staff_id = %s
        """, (pt_id, staff_id))
        connection.commit()

        # Delete the emergency_log entry
        cursor.execute("""
            DELETE FROM emergency_log
            WHERE pt_id = %s AND staff_id = %s
        """, (pt_id, staff_id))
        connection.commit()

        # Add the new interaction
        cursor.execute("INSERT INTO interactions (pt_id, staff_id, staff_notes) VALUES (%s, %s, %s)", (pt_id, staff_id, staff_notes))
        connection.commit()
        
        cursor.close()

        flash("Interaction added successfully!")
        return redirect(url_for('add_interaction'))

    return render_template('add_interaction.html')

if __name__ == '__main__':
    app.run(debug=True)