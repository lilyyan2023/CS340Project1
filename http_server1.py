import socket
# import sys
# create a TCP socket
def server1(port):
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
            data = connection_socket.recv(1024)
            if len(data) != 0:
                connection_socket.sendall(data)

                file = read_file(path)
                if file in data:
                    client.send("HTTP/1.1 200 OK\r\n")
                    client.send("Content-Type: text/html; charset=UTF-8\r\n")

                else:
                    client.send("HTTP/1.1 404 Not Found\r\n")






