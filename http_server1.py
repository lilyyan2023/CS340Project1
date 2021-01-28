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
    # accept
    while True:
        connection_socket, client = accept_socket.accept()
        # loop
        while True:
            data = connection_socket.recv(1024)
            # if len(data) != 0:
            #     print(data)
            # else:
            #     break
            print(data)
            data_str = data.decode('utf-8')
            if data_str.endswith("\r\n\r\n"):
            #receive byte array，GET request
            # convert it to string
            #     data_str = data.decode('utf-8')
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
                file = open(path[1:])
                print(file)
                if path.endswith(".htm") or path.endswith(".html"):
                    print("sending 200")

                    connection_socket.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))
                    connection_socket.send(("Content-Type: text/html; charset=UTF-8\r\n").encode('utf-8'))
                    connection_socket.send(file.read().encode('utf-8'))
                    file.close()
                else:
                    print("sending 403")
                    connection_socket.send(("HTTP/1.1 403 Forbidden\r\n").encode('utf-8'))
                    file.close()
            except Exception as e:
                print(e)
                print("sending 404")
                connection_socket.send(("HTTP/1.1 404 Not Found\r\n").encode('utf-8'))

            finally:
                connection_socket.close()
                break
server1(2005)





