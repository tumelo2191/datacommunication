import cv2
import socket
import numpy as np
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.3.143', 8000))

try:
    while True:
        # Receive data length
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

        # Process the received data (for example, display it using OpenCV)
        cv2.imshow("Received Data", data)
        cv2.waitKey(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    # Close the connection on keyboard interrupt
    client_socket.close()
