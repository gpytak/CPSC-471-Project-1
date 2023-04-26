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

            # Send the verified command to the server
            clientSocket.send(user_input.encode())

        ###################################################################################

        # Verify if the command is 'get'
        if verify_command == "get":

            if file_name != None:

                # Send the verified command and file name to the server
                clientSocket.send(user_input.encode())

                # The buffer to all data received from the client
                fileData = ""

                # The temporary buffer to store the received data
                recvBuff = ""

                # The size of the incoming file
                fileSize = 0

                # The buffer containing the file size
                fileSizeBuff = ""

                # get the size of the buffer indicated by the first 10 bytes
                fileSizeBuff = recvAll(clientSocket, 10)

                # Get the file size as an integer
                fileSize = int(fileSizeBuff)

                if fileSize == 0000000000:
                    print("[-] File '", file_name, "' does not exist.")
                    print("[-] Please enter the command in the correct format: 'get <filename>'")

                else:

                    # Get the file data using the first 10 bytes
                    fileData = recvAll(clientSocket, fileSize)

                    print("[+] Filename:", file_name)
                    print("[+] Received", fileSize, "bytes.")

            else:

                print("[-] File '", file_name, "' does not exist.")
                print("[-] Please enter the command in the correct format: 'get <filename>'")

        ###################################################################################

        # Verify if the command is 'put'
        if verify_command == "put":

            if os.path.isfile(file_name) == False:

                print("[-] File'", file_name, "'does not exist.")
                print("[-] Please enter the command in the correct format: 'put <filename>'")

                # Send the verified command and file name to the server
                clientSocket.send(user_input.encode())

            elif os.path.isfile(file_name) or file_name != None:

                # Open the file
                fileObj = open(file_name, "r")

                # Send the verified command and file name to the server
                clientSocket.send(user_input.encode())

                # The number of bytes sent
                numSent = 0

                # The file data
                fileData = None

                # Keep sending until all is sent
                while True:

                    # Read the data
                    fileData = fileObj.read(bufferSize)

                    # Make sure we did not hit EOF
                    if fileData:

                        # get the size of the data
                        dataSizeStr = str(len(fileData))

                        # makes sure the dataSize is 10
                        while len(dataSizeStr) < 10:
                            dataSizeStr = "0" + dataSizeStr

                        # add the data size before the rest of the command
                        fileData = dataSizeStr + fileData

                        # The number of bytes sent
                        numSent = 0

                        # Send the data!
                        while len(fileData) > numSent:
                            numSent += clientSocket.send(
                                fileData[numSent:].encode())

                    else:
                        # Close the file because we're done
                        fileObj.close()
                        break

                print("[+] Filename:", file_name)
                print("[+] Sent", numSent, "bytes.")

            else:

                print("[-] File'", file_name, "'does not exist.")
                print("[-] Please enter the command in the correct format: 'put <filename>'")

        ###################################################################################

        # Verify if the command is 'ls'
        if verify_command == "ls":

            # Send the verified command to the server
            clientSocket.send(verify_command.encode())

        ###################################################################################

        # Verify if the command is 'quit'
        if verify_command == "quit":

            # Send the verified command to the server
            clientSocket.send(verify_command.encode())

            # Close the socket
            clientSocket.close()

            break
