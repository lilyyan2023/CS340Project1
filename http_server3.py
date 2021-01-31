import socket
import sys

port = int(sys.argv[1])
def server3(port):
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
            data_str = data.decode('utf-8')
            if data_str.endswith("\r\n\r\n"):
                print(data_str)
                #Split data with ' ', then jump accross "/product" by [10:], and split with "&" 
                request = data_str.split(' ')[1][10:].split("&")
                operands = []
                result = 1
                #create operands and result
                for i in request:
                    operands.append(i.split("=")[1])
                    print(operands)
                    result *= float(i.split("=")[1])
                print("sending 200")
                connection_socket.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))
                connection_socket.send(("Content-Type: text/html; charset=UTF-8\r\n\r\n").encode('utf-8'))
                connection_socket.send(str(result).encode('utf-8'))
                #else:
                    #print("sending 403")
                    #connection_socket.send(("HTTP/1.1 403 Forbidden\r\n\r\n").encode('utf-8'))
                #print("sending 404")
                #connection_socket.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode('utf-8'))
            #finally:
                connection_socket.close()
                break
server3(port)





