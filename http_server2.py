import socket
import sys
import select
import queue
port = int(sys.argv[1])
def server2(port):
    # create a TCP socket
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    accept_socket.setblocking(0) #?
    #bind socket
    address = ("", port) #?
    accept_socket.bind(address)
    #listen, not specifying the backlog
    accept_socket.listen(5)
    #initialize list of open connections
    # open_connections = []
    # list of sockets waiting to read
    read_list = []
    # add accept_socket to read list
    read_list.append(accept_socket)
    # initialize an output
    outputs = []
    # initialize a dictionary
    message_queues = {}
    while True:
        # # list of sockets waiting to read
        # read_list = []
        # # add accept_socket to read list
        # read_list.append(accept_socket)
        # # initialize an output
        # outputs = []
        # call select
        readable, writable, exceptional = select.select(read_list, outputs, read_list)
        print(readable)
        print(writable)
        print(exceptional)


        # iterate readable sockets on the read list

        for r in readable:
            # if it's the accept socket
            if r is accept_socket:
                print("it is the accept socket")
                #accept new connection
                connection_socket, client_address = r.accept()
                #change it to blocking state?
                connection_socket.setblocking(0)
                # add to list of open_connections
                read_list.append(connection_socket)
                print(connection_socket)
                message_queues[connection_socket] = queue.Queue()
                print(message_queues)
            else:
                # connection_socket, client_address = r.accept()
                data = r.recv(1024)
                # print(data)
                print(message_queues)
                if data:
                    message_queues[r].put(data)
                    if r not in outputs:
                        outputs.append(r)
                else:
                    if r in outputs:
                        outputs.remove(r)
                    read_list.remove(r)
                    r.close()
                    del message_queues[r]

        for w in writable:
            try:
                next_msg = message_queues[w].get_nowait()
                # print(next_msg)

            except queue.Empty:
                outputs.remove(w)
            else:

                data_str = next_msg.decode('utf-8')
                print(data_str)
                if data_str.endswith("\r\n\r\n"):
                    print("debug")
                    request = data_str.split(' ')
                    path = request[1]
                    print(path)
                try:
                    file = open(path[1:])
                    print(file)
                    if path.endswith(".htm") or path.endswith(".html"):
                        print("sending 200")
                        w.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))
                        w.send(("Content-Type: text/html; charset=UTF-8\r\n\r\n").encode('utf-8'))
                        w.send(file.read().encode('utf-8'))
                        file.close()
                    else:
                        print("sending 403")
                        w.send(("HTTP/1.1 403 Forbidden\r\n\r\n").encode('utf-8'))
                        file.close()
                except Exception as e:
                    print(e)
                    print("sending 404")
                    w.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode('utf-8'))

                finally:
                    print("close")
                    # w.close()
                    print("remove")
                    read_list.remove(w)
                    break
                w.send(next_msg)
                w.close()
        for e in exceptional:
            read_list.remove(e)
            if e in outputs:
                outputs.remove(e)
            e.close()
            del message_queue[e]

                # data_str = data.decode('utf-8')
                # if data_str.endswith("\r\n\r\n"):
                #     request = data_str.split(' ')
                #     path = request[1]
                # try:
                #     file = open(path[1:])
                #     print(file)
                #     if path.endswith(".htm") or path.endswith(".html"):
                #         print("sending 200")
                #         connection_socket.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))
                #         connection_socket.send(("Content-Type: text/html; charset=UTF-8\r\n").encode('utf-8'))
                #         connection_socket.send(file.read().encode('utf-8'))
                #         file.close()
                #     else:
                #         print("sending 403")
                #         connection_socket.send(("HTTP/1.1 403 Forbidden\r\n").encode('utf-8'))
                #         file.close()
                # except Exception as e:
                #     print(e)
                #     print("sending 404")
                #     connection_socket.send(("HTTP/1.1 404 Not Found\r\n").encode('utf-8'))
                #
                # finally:
                #     connection_socket.close()
                #     open_connections.remove(connection_socket)
                #     break
server2(port)


