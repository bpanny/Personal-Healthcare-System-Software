Sure, here’s the modified code that uploads messages to a PostgreSQL database and sends an emergency message when the message is “help”. Please replace the database credentials and Twilio API credentials with your own.

import cv2
import urllib.request
import numpy as np
import time
import psycopg2
from twilio.rest import Client

url = 'http://10.0.0.184:8080/shot.jpg'

# Load the cascade
hand_cascade = cv2.CascadeClassifier('hand.xml')

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="myuser",
    password="mypassword"
)

# Create a cursor object
cur = conn.cursor()

# Connect to Twilio API
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect hands
    hands = hand_cascade.detectMultiScale(gray, 1.1, 4)

    # If hands are detected, send "help" message and store in database
    if len(hands) > 0:
        message = "help"
        cur.execute("INSERT INTO messages (message, time) VALUES (%s, %s)", (message, time.time()))
        conn.commit()
        client.messages.create(
            body=message,
            from_='your_twilio_number',
            to='your_phone_number'
        )
    else:
        message = "safe"
        cur.execute("INSERT INTO messages (message, time) VALUES (%s, %s)", (message, time.time()))
        conn.commit()

    time.sleep(5)