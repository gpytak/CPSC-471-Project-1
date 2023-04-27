# CPSC-471-Project-1
Daniel Chen Wu as d.wu@csu.fullerton.edu  
Jose Morales as j_morales@csu.fullerton.com  
Gregory Pytak as gpytak@csu.fullerton.edu  
Luis Venegas as Luisvenegas214@csu.fullerton.edu  
Daniel Yoshida as dtyoshid@csu.fullerton.edu
## Programming language used: Python
## Follow the steps below to execute this code using python3:
1) Unzip the tar file and place/save the folder "CPSC-471-Project-1-main" in the downloads folder.
1) Open a terminal and cd into the server folder, "cd Downloads/CPSC-471-Project-1-main/server".
2) Open a second terminal and cd into the client folder, "cd Downloads/CPSC-471-Project-1-main/client".
3) Invoke the server before invoking the client.
4) Use the server terminal and the server shall be invoked as: python3 serv.py "port number" Example: python3 serv.py 12001
5) Use the client terminal and the ftp client is invoked as: python3 cli.py "server machine" "server port" Example: python3 cli.py localhost 12001
6) The user can use the following commands when ftp> is prompted in the client terminal:
```
ftp> get <filename>
ftp> put <filename>
ftp> ls
ftp> quit
```
### All invalid inputs are checked and reprompts the user for a correct input
