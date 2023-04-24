# python client.py 127.0.0.1 12001

import socket
import os
import sys

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


# Sends the address of the server
serverAddress = str(sys.argv[1])

# Sends the port number of the server
serverPort = int(sys.argv[2])

# Command line checks (Needs to be resolved)
if len(sys.argv) < 2:
    print("USAGE python " + sys.argv[0] + " <FILE NAME>")

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
clientSocket.connect((serverAddress, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = None

# Buffer size
bufferSize = 4096

# Keep sending until all is sent
while True:

    # Receives the user's input
    user_input = input("ftp> ")

    # Separate the "ftp>" and "command"
    command = user_input.split(" ")

    ###################################################################################

    # ftp> line check for ls and quit
    if len(command) == 1 and (command[0] == "ls" or command[0] == "quit"):
        # Gets the individual command from the input (Example: ls file.txt) -> Output: ls
        verify_command = command[0]

    # ftp> line check for put and get
    elif len(command) > 1 and (command[0] == "put" or command[0] == "get"):
        # Gets the individual command from the input (Example: ls file.txt) -> Output: ls
        verify_command = command[0]
        # Gets the file name from the input (Example: ls file.txt) -> Output: file.txt
        file_name = command[1]

    # ftp> line check error message
    else:
        print("Please enter the command(s) in the correct format: 'put <filename>' or 'get <filename>' or 'ls' or 'quit'")
        break

    ###################################################################################

    # Verify if the command is 'get'
    if verify_command == "get":

        try:
            # Get the file size
            fileSize = os.path.getsize(file_name)
        except:
            print("Unable to get file size")
            break

        # Send the verified command to the server
        clientSocket.send(verify_command.encode())

    ###################################################################################

    # Verify if the command is 'put'
    if verify_command == "put":

        # Check to see if the file is available or not
        try:
            # Open the file
            fileObj = open(file_name, "r")
            print("Was able to open file")
        except:
            print("Unable to locate file")
            break

        # Send the verified command to the server
        clientSocket.send(verify_command.encode())

        # Read 65536 bytes of data
        fileData = fileObj.read(65536)

        # Make sure we did not hit EOF
        if fileData:

            # Get the size of the data read
            # and convert it to string
            dataSizeStr = str(len(fileData))

            # Prepend 0's to the size string
            # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Prepend the size of the data to the
            # file data.
            fileData = dataSizeStr + fileData

            # The number of bytes sent
            numSent = 0

            # Send the data!
            while len(fileData) > numSent:
                numSent += clientSocket.send(fileData[numSent:])

        # The file has been read. We are done
        else:
            fileObj.close()
            break

        print("Filename:", file_name)
        print("Sent ", numSent, " bytes.")

    ###################################################################################

    # Verify if the command is 'ls'
    if verify_command == "ls":
        # Send the verified command to the server
        clientSocket.send(verify_command.encode())

        receivedData = clientSocket.recv(bufferSize).decode()

    ###################################################################################

    # Verify if the command is 'quit'
    if verify_command == "quit":
        # Close the socket and the file
        clientSocket.close()
        break

# Close the socket
clientSocket.close()
