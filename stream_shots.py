import urllib.request
import cv2
import numpy as np
import time
from datetime import datetime
import uploader

# Define the send_message function
def send_message(pt_id, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        "pt_id": pt_id,
        "message": message,
        "timestamp": timestamp
    }
    uploader.uploader(message_data)

# Load the cascade classifier for hand detection
hand_cascade = cv2.CascadeClassifier("hand.xml")

# URL of the livestream
url = "http://10.0.0.184:8080/shot.jpg"
pt_id = 1
# Create a loop that fetches the latest frame every 2 seconds
while True:
    # Open the URL using urllib and convert the response into a NumPy array
    img_arr = np.array(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)
    
    # Decode the NumPy array to an image
    img = cv2.imdecode(img_arr, -1)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect hands in the image using the cascade classifier
    hands = hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if hands are detected or not
    if len(hands) > 0:
        print("help")
        send_message(pt_id, "help")
    else:
        print("safe")
        send_message(pt_id, "safe")

    # Wait for 2 seconds before fetching the next frame
    time.sleep(2)

    # If 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
