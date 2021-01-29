import socket
import sys


def fetch_data(addr,size):
    #Cited from https://stackoverflow.com/questions/34192093/python-socket-get
    sock = socket.socket()
    sock.connect((socket.gethostbyname(addr),80))
    sock.send(bytes"GET / HTTP/1.1\r\nHost: "+socket.gethostbyname(addr)+"\r\n\r\n","utf-8"))
    message = sock.recv(size)
    sock.close()
    return(message.decode())
    

name = str(sys.argv[1])
output = sys.stdout
errMsg = sys.stderr
if name[0:7] != "http://":
    errMsg.write('error')
    sys.exit(1)
else:
    #Fetch content length
    size = 1024
    response = fetch_data(name[7:],size).split("\r\n")
    header_counter = 0
    content_length = -1
    while response[header_counter] != "":
        header_counter += 1
        if(header_counter > len(response)):
            print("should not see")
            size += 1024
            response = fetch_data(name[7:],size).split("\r\n")
    for i in range(0,header_counter):
        line = response[i].split(": ")
        if line[0] == "Content-Length":
            content_length = int(line[1])
    #Print entity
    response = fetch_data(name[7:],content_length).split("\r\n")
    for i in range(header_counter, len(response)-1):
        output.write(response[i])
    sys.exit(0)
