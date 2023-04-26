import socket
import sys
import subprocess
import time

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

    def getUserInput():

        # Gets the command from the client
        receivedData = clientSocket.recv(bufferSize).decode()

        command = receivedData.split(" ")

        ###################################################################################

        if command[0] == "get":

            # Check to see if the file is available or not
            try:
                # Open the file
                fileObj = open(command[1], "r")
                print("[+] Was able to open file")
            except:
                print("[-] Unable to locate file")

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

            print("-----------")
            print("get")
            print("[+] Sent", numSent, "bytes.")
            print("[+] SUCCESS")

            getUserInput()

        ###################################################################################

        if command[0] == "put":

            # The buffer to all data received from the client
            fileData = ""

            # The size of the incoming file
            fileSize = 0

            # The buffer containing the file size
            fileSizeBuff = ""

            # get the size of the buffer indicated by the first 10 bytes
            fileSizeBuff = recvAll(clientSocket, 10)

            # Get the file size as an integer
            fileSize = int(fileSizeBuff)

            # Get the file data using the first 10 bytes
            fileData = recvAll(clientSocket, fileSize)

            print("-----------")
            print("put")
            print("[+] Received", fileSize, "bytes.")
            print("[+] SUCCESS")

            getUserInput()

        ###################################################################################

        if command[0] == "ls":
            for line in subprocess.getstatusoutput(command[0]):
                print(line)

            print("-----------")
            print("ls")
            print("[+] SUCCESS")

            getUserInput()

        ###################################################################################

        if command[0] == "quit":

            print("-----------")
            print("quit")
            print("[+] SUCCESS")

            # Close the socket and the file
            clientSocket.close()

            exit()

    print("Waiting for connections...")

    # Accept connections
    clientSocket, addr = serverSocket.accept()

    with clientSocket:

        print("Accepted connection from client: ", addr)
        print("\n")

        getUserInput()
