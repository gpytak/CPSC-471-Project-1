
# Client code
import socket

# Name and port number of the server to which want to connect .
#serverName = 'ecs.fullerton.edu'
#serverName = '10.67.86.205'
serverName = '127.0.0.1'
serverPort = 12000
# Create a socket
clientSocket = socket.socket (socket.AF_INET , socket.SOCK_STREAM)
# Connect to the server
clientSocket.connect (( serverName , serverPort ))
# A string we want to send to the server
data = "Hello world! This is a very long string. "
bytesSent = 0

# Keep sending bytes until all bytes are sent
while bytesSent != len ( data ) :
# Send that string !
    print("sending message")
    bytesSent += clientSocket.send (data.encode()) 
    #bytesSent += clientSocket.send(data[bytes sent])
# Close the s ocket
clientSocket.close ()
print("end of this program")