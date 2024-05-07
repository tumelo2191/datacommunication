from flask import Flask, render_template, Response,request, jsonify
import cv2
import socket
import numpy as np
import pickle
from azure.storage.queue import QueueClient

# Azure Queue Storage credentials
connection_string = "DefaultEndpointsProtocol=https;AccountName=serialcomms;AccountKey=jLtYi6hcYE/+ObmLkOGs9SXaRSP/0wdNZWfkX82+BcoVVzBhKpgF4rPBSbtbmyP3rLWAHnQe/WDM+AStt2AWoA==;EndpointSuffix=core.windows.net"
queue_name = "serialcommqueue"

queue_client = QueueClient.from_connection_string(connection_string, queue_name)

# Initialize socket


app = Flask(__name__)


print("1")

#
#
# # Initialize the webcam
# print("2")


def gen_frames():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.3.143', 8000))
    while True:
        data_length_bytes = client_socket.recv(4)
        if not data_length_bytes:
            break  # Exit the loop if no more data is received
        data_length = int.from_bytes(data_length_bytes, byteorder='big')

        # Receive data
        data_serialized = b''
        while len(data_serialized) < data_length:

            chunk = client_socket.recv(data_length - len(data_serialized))
            if not chunk:
                break  # Exit the loop if no more data is received
            data_serialized += chunk

        # Deserialize the received data
        data = pickle.loads(data_serialized)
        ret, buffer = cv2.imencode('.jpg', data)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        #cv2.imshow("Received Data", data)he received data (for example, display it using OpenCV)




def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            print("Unsuccessful")
            break
        else:
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            print("Successful")
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # Press 'q' to exit the loop

def capture_frame(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Display the frame or perform any other processing
            cv2.imshow('Front Camera', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
@app.route('/place_message_in_queue', methods=['POST'])
def place_message_in_queue():
    message = request.json.get('message')
    queue_client.send_message(message)
    return jsonify({'message': message})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_image')
def take_photo():
    return Response(capture_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
