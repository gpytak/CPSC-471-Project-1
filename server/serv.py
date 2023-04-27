import socket
import sys
import subprocess
import os.path

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

            # Check if the length of the command is 3
            if len(receivedData) == 3:

                print("-----------")
                print("[-] FAILURE")

                getUserInput()

            # Check if the path of the file exists or not
            if os.path.isfile(command[1]):

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

            if len(receivedData) != 3:

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

                with open(command[1], 'w') as file:
                    file.write(fileData)

                print("-----------")
                print("[+] SUCCESS")

                getUserInput()

            else:

                print("-----------")
                print("[-] FAILURE")

                getUserInput()

        ###################################################################################

        # Verify if the command is 'ls'
        elif command[0] == "ls":

            for line in subprocess.getstatusoutput(command[0]):
                print(line)

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
