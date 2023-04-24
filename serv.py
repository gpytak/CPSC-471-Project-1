import socket
import sys
import subprocess

# Command line checks
if len(sys.argv) != 2:
    print("USAGE: python3 serv.py <port number>")

else:
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
            tmpBuff = sock.recv(numBytes).decode()

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

        # Gets the command from the client
        receivedData = clientSocket.recv(bufferSize).decode()

        print(receivedData)

        ###################################################################################

        if receivedData == "get":

            # Gets the file name from the client
            receivedFileName = clientSocket.recv(bufferSize).decode()

            # Check to see if the file is available or not
            try:
                # Open the file
                fileObj = open(receivedFileName, "r")
                print("[+] Was able to open file")
            except:
                print("[-] Unable to locate file")
                break

            # The number of bytes sent
            numSent = 0

            # The file data
            fileData = None

            # Keep sending until all is sent
            while True:

                # Read the data
                fileData = fileObj.read(65536)

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
                        numSent += clientSocket.send(fileData[numSent:].encode())

                else:
                    # close the file because we're done
                    fileObj.close()
                    break

            print("[+] Sent", numSent, "bytes.")
            print("[+] SUCCESS")

            # Close the socket and the file
            clientSocket.close()
            break

        ###################################################################################

        if receivedData == "put":
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

            # first 10 bytes indicate the file's size so we get that
            fileSizeBuff = recvAll(clientSocket, 10)

            # convert the file size to an integer
            fileSize = int(fileSizeBuff)

            print("[+] Received", fileSize, "bytes.")
            print("[+] SUCCESS")

            # Close the socket and the file
            clientSocket.close()
            break

        ###################################################################################

        if receivedData == "ls":
            for line in subprocess.getstatusoutput(receivedData):
                print(line)

            print("[+] SUCCESS")

            # Close the socket and the file
            clientSocket.close()
            break

        ###################################################################################

        if receivedData == "quit":
            print("[+] SUCCESS")

            # Close the socket and the file
            clientSocket.close()
            break

    serverSocket.close()
