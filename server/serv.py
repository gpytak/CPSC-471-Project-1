import socket
import sys
import os.path
from sys import getsizeof

# Command line checks
if len(sys.argv) != 2:
    print("USAGE: python3 serv.py <port number>")

else:
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
            tmpBuff = sock.recv(numBytes).decode()

            # The other side has closed the socket
            if not tmpBuff:
                break

            # Add the received bytes to the buffer
            recvBuff += tmpBuff

        return recvBuff

    # Gets the port number of the server
    serverPort = int(sys.argv[1])

    # Create a TCP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    serverSocket.bind(('', serverPort))

    print("Ephemeral port: ", serverSocket.getsockname()[1])

    # Start listening for incoming connections
    serverSocket.listen(1)

    # Buffer size
    bufferSize = 4096

    # Getting the path of the folder
    sys.path.insert(0, "..")

    def getUserInput():

        # Gets the command and/or file name from the client
        receivedData = clientSocket.recv(bufferSize).decode()

        # Separates the command and file name
        command = receivedData.split(" ")

        ###################################################################################

        # Verify if the command is 'get'
        if command[0] == "get":

            # Check if the length of the command is 3 or the file name is empty
            if len(receivedData) == 3 or command[1] == None:

                print("-----------")
                print("[-] FAILURE")

                getUserInput()

            # Check if the path of the file exists or not
            if os.path.isfile(command[1]) == True:

                # Open the file
                fileObj = open(sys.path[1] + "/" + command[1], "r")

                # The number of bytes sent
                numSent = 0

                # The file data
                fileData = None

                # Set a flag for 0 byte
                zeroFilesent = False

                # Keep sending until all is sent
                while True:

                    # Read the data
                    fileData = fileObj.read(bufferSize)

                    # Make sure we did not hit EOF
                    if fileData:

                        # Get the size of the data
                        dataSizeStr = str(len(fileData))

                        # Makes sure the dataSize is 10
                        while len(dataSizeStr) < 10:
                            dataSizeStr = "0" + dataSizeStr

                        # Add the data size before the rest of the command
                        fileData = dataSizeStr + fileData

                        # The number of bytes sent
                        numSent = 0

                        # Send the data!
                        while len(fileData) > numSent:
                            numSent += clientSocket.send(
                                fileData[numSent:].encode())

                    # File exists but is 0 byte
                    elif os.stat(command[1]).st_size == 0 and zeroFilesent == False:

                        dataSizeStr = "0"

                        # Makes sure the dataSize is 10
                        while len(dataSizeStr) < 10:
                            dataSizeStr = "0" + dataSizeStr

                        # Add the data size before the rest of the command
                        fileData = dataSizeStr + fileData

                        # The number of bytes sent
                        numSent = 0

                        # Send the data!
                        while len(fileData) > numSent:
                            numSent += clientSocket.send(
                                fileData[numSent:].encode())

                        zeroFilesent = True

                    else:
                        # Close the file because we're done
                        fileObj.close()
                        break

                print("-----------")
                print("[+] SUCCESS")

                getUserInput()

            else:

                print("-----------")
                print("[-] FAILURE")

                getUserInput()

        ###################################################################################

        # Verify if the command is 'put'
        elif command[0] == "put":

            # Check if the length of the command is 3 or the file name is empty
            if len(receivedData) == 3 or command[1] == None:

                print("-----------")
                print("[-] FAILURE")

                getUserInput()

            # Getting the path of the folder
            print('Current Working Directory is: ', os.getcwd())

            # Move to client directory
            os.chdir('..\client/')

            # Confirm the current directory
            print('Updated Working Directory is: ', os.getcwd())

            if os.path.isfile(command[1]) == True:

                # The buffer to all data received from the client
                fileData = ""

                # The size of the incoming file
                fileSize = 0

                # The buffer containing the file size
                fileSizeBuff = ""

                # Get the size of the buffer indicated by the first 10 bytes
                fileSizeBuff = recvAll(clientSocket, 10)

                # Get the file size as an integer
                fileSize = int(fileSizeBuff)

                # Get the file data using the first 10 bytes
                fileData = recvAll(clientSocket, fileSize)

                # Getting the path of the folder
                print('Current Working Directory is: ', os.getcwd())

                # Move to server directory
                os.chdir('..\server/')

                # Confirm the current directory
                print('Updated Working Directory is: ', os.getcwd())

                # Generate file
                with open(command[1], 'w') as file:
                    file.write(fileData)

                print("-----------")
                print("[+] SUCCESS")

                getUserInput()

            else:

                print("-----------")
                print("[-] FAILURE")

                # Move to server directory
                os.chdir('..\server/')

                getUserInput()

        ###################################################################################

        # Verify if the command is 'ls'
        elif command[0] == "ls":

            # This create a list and sort it
            lsString = os.listdir("./")
            lsString.sort()

            # Concatenate it in a string
            fileData = ""
            for file in lsString:

                # Discard folders
                if os.path.isfile(file):
                    fileData += file + " -> " + \
                        str(os.path.getsize(file)) + " bytes\n"
                else:
                    fileData += "\\" + file + "\n"

            # The number of bytes sent
            numSent = 0

            # FileHeader will change to receive a header
            fileHeader = fileData

            # Get the size of the data
            dataSizeStr = str(len(fileData))

            # Makes sure the dataSize has 10 digits
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Add the data size before the rest of the command
            fileHeader = dataSizeStr + fileHeader

            # The number of bytes sent
            numSent = 0

            # Send the data!
            while len(fileData) > numSent:
                numSent += clientSocket.send(
                    fileHeader[numSent:].encode())

            print(fileData)

            print("-----------")
            print("[+] SUCCESS")

            getUserInput()

        ###################################################################################

        # Verify if the command is 'quit'
        elif command[0] == "quit":

            print("-----------")
            print("[+] SUCCESS")

            # Close the sockets
            clientSocket.close()
            serverSocket.close()

            exit()

        else:

            print("-----------")
            print("[-] FAILURE")

            getUserInput()

    print("Waiting for connections...")

    # Accept connections
    clientSocket, addr = serverSocket.accept()

    with clientSocket:

        print("Accepted connection from client: ", addr)
        print("\n")

        getUserInput()
