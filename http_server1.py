import socket
import sys

def server1(port):
    # create a TCP socket
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind socket
    address = ("", port) #?
    accept_socket.bind(address)
    #listen
    accept_socket.listen(1)
    #loop
    while True:
        #break
        connection_socket, client = accept_socket.accept()
        data = connection_socket.recv(1024)
        if len(data) != 0:
            print(data)
        else:
            break
        #receive byte array，GET request

        # convert it to string
    data_str = data.decode('utf-8')
    request = data_str.split(' ')
    path = request[1]
            # print(data_str)
            # if len(data_str) != 0:
            #     print(data_str)
            # else:
            #     break
            # connection_socket.sendall(data)
            # get path
        # path = data_str[3:]
        # print(path)
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
# server1(8000)





