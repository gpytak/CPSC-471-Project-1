# python server.py 12001

# Server code
import socket
import sys

# Gets the port number of the server
serverPort = int(sys.argv[1])

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
serverSocket.bind(('', serverPort))

# Start listening for incoming connections
serverSocket.listen(1)

print("The server is ready to receive")
# The buffer to store the received data
data = ""

# Forever accept incoming connections
while 1:
 # Accept a connection ; get client’ s socket
    connectionSocket, addr = serverSocket.accept()
    print("connection from " + socket.gethostname())
    # The temporary buffer
    tmpBuff = ""
    while len(data) != 40:
        tmpBuff = connectionSocket.recv(40).decode()
        # print(tmpBuff)
# The other side unexpectedly closed it’s socket
        if not tmpBuff:
            break
# Save the data
        data += tmpBuff
    print(data)

    # Close the socket
    connectionSocket.close()
print("end of server")
