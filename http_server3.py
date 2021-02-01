import socket
import sys
import json

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
                # if a user requests /product url
                print(data_str.split(' ')[1][:8] == "/product")
                if data_str.split(' ')[1][:8] == "/product":
                    # print(data_str.split(' ')[1].split("=")[1])
                    # content = data_str.split(' ')[1].split("=")[1]

                    if len(data_str.split(' ')[1].split("?"))!= 1 and data_str.split(' ')[1].split("=")[1].split("&")[0].isnumeric():

                        #Split data with ' ', then jump accross "/product" by [10:], and split with "&"
                        request = data_str.split(' ')[1][10:].split("&")
                        operands = []
                        result = 1
                        #create operands and result
                        for i in request:
                            operands.append(i.split("=")[1])
                            print(operands)
                            result *= float(i.split("=")[1])
                        dict = {}
                        dict["operation"] = "product"
                        dict["operands"] = operands
                        # how do we know whether it overflows
                        if result != float("inf") and result != float("-inf"):
                            dict["result"] = result
                        elif result == float("inf"):
                            dict["result"] = "inf"
                        else:
                            dict["result"] = "-inf"
                        dict_json = json.dumps(dict)

                        print("sending 200")
                        connection_socket.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))
                        connection_socket.send(("Content-Type: application/json\r\n\r\n").encode('utf-8'))
                        # do we need to encode?
                        connection_socket.send(dict_json.encode('utf-8'))
                    # if after /product, there is nothing or is not a number
                    else:
                        print("sending 400")
                        connection_socket.send(("HTTP/1.1 400 Bad Request\r\n\r\n").encode('utf-8'))
                else:
                    print("sending 404")
                    connection_socket.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode('utf-8'))
            connection_socket.close()
            break
server3(port)





