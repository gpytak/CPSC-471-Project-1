# python server.py 12001

import socket
import sys
import os
import subprocess

# Gets the port number of the server
serverPort = int(sys.argv[1])

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
serverSocket.bind(('', serverPort))

# Start listening for incoming connections
serverSocket.listen(1)

# Buffer size
bufferSize = 4096

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

    # The buffer
    recvBuff = ""

    # The temporary buffer
    tmpBuff = ""

    # Keep receiving till all is received
    while len(recvBuff) < numBytes:

        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes)

        # The other side has closed the socket
        if not tmpBuff:
            break

        # Add the received bytes to the buffer
        recvBuff += tmpBuff

    return recvBuff


# Accept connections forever
while True:

    print("Waiting for connections...")

    # Accept connections
    clientSocket, addr = serverSocket.accept()

    print("Accepted connection from client: ", addr)
    print("\n")

    receivedData = clientSocket.recv(bufferSize).decode()
    print(receivedData)

    ###################################################################################

    if receivedData == "get":
        print("SUCCESS")

    ###################################################################################

    elif receivedData == "put":
        print("SUCCESS")

    ###################################################################################

    elif receivedData == "ls":
        for line in subprocess.getstatusoutput(receivedData):
            print(line)

        print("SUCCESS")

    else:
        break

    # The buffer to all data received from the
    # the client.
    fileData = ""

    # The temporary buffer to store the received
    # data.
    recvBuff = ""

    # The size of the incoming file
    fileSize = 0

    # The buffer containing the file size
    fileSizeBuff = ""

    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(clientSocket, 10)

    # Get the file size
    fileSize = int(fileSizeBuff)

    print("The file size is ", fileSize)

    # Get the file data
    fileData = recvAll(clientSocket, fileSize)

    print("The file data is: ")
    print(fileData)

    # Close our side
    clientSocket.close()
