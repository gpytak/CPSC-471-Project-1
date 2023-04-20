# python client.py 127.0.0.1 12001

# Client code
import socket
import sys

# Sends the address of the server
serverAddress = str(sys.argv[1])

# Sends the port number of the server
serverPort = int(sys.argv[2])

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
try:
    clientSocket.connect((serverAddress, serverPort))
    # A string we want to send to the server
    data = "Hello world! This is a very long string. "
    bytesSent = 0
    print("trying to send")

    # Keep sending bytes until all bytes are sent
    while bytesSent != len(data):
        # Send that string !
        print("sending message")
        bytesSent += clientSocket.send(data.encode())
        # bytesSent += clientSocket.send(data[bytes sent])

except:
    print("Connection to the server could not be established.\nCheck IP and PORT from the server.")

# Close the socket
clientSocket.close()
