import socket
import sys
import os.path

# Command line checks
if len(sys.argv) != 3:
    print("USAGE: python3 cli.py <server machine> <server port>")

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

    # Buffer size
    bufferSize = 4096

    # Sends the address of the server
    serverAddress = sys.argv[1]

    # Sends the port number of the server
    serverPort = int(sys.argv[2])

    # Create a socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    clientSocket.connect((serverAddress, serverPort))

    # Getting the path of the folder
    sys.path.insert(0, "..")

    # Keep sending until all is sent
    while True:

        # Receives the user's input
        user_input = input("ftp> ")

        # Separate the "ftp>" and "command"
        command = user_input.split(" ")

        verify_command = ""

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

            print("[-] Please enter the command(s) in the correct format: 'put <filename>' or 'get <filename>' or 'ls' or 'quit'")

            # Send the user_input command to the server
            clientSocket.send(user_input.encode())

        ###################################################################################

        # Verify if the command is 'get'
        if verify_command == "get":

            if file_name != None:

                # Send the user_input command and file name to the server
                clientSocket.send(user_input.encode())

                # The buffer to all data received from the client
                fileData = ""

                # The temporary buffer to store the received data
                recvBuff = ""

                # The size of the incoming file
                fileSize = 0

                # The buffer containing the file size
                fileSizeBuff = ""

                # Get the size of the buffer indicated by the first 10 bytes
                fileSizeBuff = recvAll(clientSocket, 10)
                
                #check if the header contains the file size or an error message
                if fileSizeBuff == "FFFFFFFFFF":
                    print("[-] File '", file_name, "' does not exist.")
                else:
                    # Get the file size as an integer
                    fileSize = int(fileSizeBuff)

                    # Get the file data using the first 10 bytes
                    fileData = recvAll(clientSocket, fileSize)

                    with open(file_name, 'w') as file:
                        file.write(fileData)

                    print("[+] Filename:", file_name)
                    print("[+] Received", fileSize, "bytes.")

            else:
                print("[-] Please enter the command in the correct format: 'get <filename>'")

                # Send the user_input command and file name to the server
                clientSocket.send(user_input.encode())

        ###################################################################################

        # Verify if the command is 'put'
        if verify_command == "put":

            # Check if the path of the file exists or not
            if os.path.isfile(file_name):

                # Send the user_input command and file name to the server
                clientSocket.send(user_input.encode())

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

                print("[+] Filename:", file_name)
                print("[+] Sent", numSent, "bytes.")

            else:

                print("[-] File'", file_name, "'does not exist.")

                # Send the user_input command and file name to the server
                clientSocket.send(user_input.encode())

        ###################################################################################

        # Verify if the command is 'ls'
        if verify_command == "ls":

            # Send the verified command to the server
            clientSocket.send(verify_command.encode())

            # The buffer to all data received from the client
            fileData = ""

            # The temporary buffer to store the received data
            recvBuff = ""

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

            # Display a message and the server directory files
            print(fileData)

        ###################################################################################

        # Verify if the command is 'quit'
        if verify_command == "quit":

            # Send the verified command to the server
            clientSocket.send(verify_command.encode())

            # Close the socket
            clientSocket.close()

            break
