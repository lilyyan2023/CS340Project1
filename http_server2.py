import socket
import sys
import select

def server2(port):
    # create a TCP socket
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind socket
    address = ("", port) #?
    accept_socket.bind(address)
    #listen, not specifying the backlog
    accept_socket.listen()
    #initialize list of open connections
    open_connections = []
    while True:
        # list of sockets waiting to read
        read_list = []
        # add accept_socket to read list
        read_list.append(accept_socket)
        # initialize an output
        outputs = []
        # call select
        readable, writable, exceptional = select.select(read_list, outputs, read_list)
        # iterate readable sockets on the read list
        for r in readable:
            # if it's the accept socket
            if r is accept_socket:
               #accept new connection
               connection_socket, client_address = r.accept()
               #change it to blocking state?
               connection_socket.setblocking(0)
               # add to list of open_connections
               open_connections.append(connection_socket)
            else:
                # connection_socket, client_address = r.accept()
                data = r.recv(1024)
                print(data)
                data_str = data.decode('utf-8')
                if data_str.endswith("\r\n\r\n"):
                    request = data_str.split(' ')
                    path = request[1]
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
                    open_connections.remove(connection_socket)
                    break
server2(8304)


