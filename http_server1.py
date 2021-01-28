import socket
import sys
# create a TCP socket
def server1(port, path):
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind socket
    accept_socket.bind(port)
    #listen
    accept_socket.listen("")
    #loop
    while True:
        #break
        connection_socket, client = accept_socket.accept()

        while True:
            #receive byte array，GET request
            data = connection_socket.recv(1024)
            # convert it to string
            data_str = data.decode()
            if len(data_str) != 0:
                print(data_str)
                # connection_socket.sendall(data)
            # get path
            path = data_str[3:]
            try:
                file = open(path)
                if path.endswith(".htm") or path.endswith(".html"):
                    connection_socket.send("HTTP/1.1 200 OK\r\n")
                    connection_socket.send("Content-Type: text/html; charset=UTF-8\r\n")
                    connection_socket.send(file.read())
                else:
                    connection_socket.send("HTTP/1.1 403 Forbidden\r\n")
            except:
                connection_socket.send("HTTP/1.1 404 Not Found\r\n")
            finally:
                connection_socket.close()






