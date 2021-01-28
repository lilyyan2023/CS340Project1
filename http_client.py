import socket
import sys

name = str(sys.argv[1])
output = sys.stdout
errMsg = sys.stderr
if name[0:7] != "http://":
    errMsg.write('error')
    sys.exit(1)
else:
    sock = socket.socket()
    sock.connect((name[7:],80))
    #Cited from https://stackoverflow.com/questions/34192093/python-socket-get
    sock.send(bytes("GET / HTTP/1.1\r\nHost: "+socket.gethostbyname(name[7:])+"\r\n\r\n","utf-8"))
    #Fetch content length
    size = 1024
    message = sock.recv(size)
    header_counter = 0
    response = message.decode().split("\r\n")
    content_length = -1
    while response[header_counter] != "":
        header_counter += 1
        if(header_counter > len(response)):
            print("should not see")
            size += 1024
            sock.send(bytes("GET / HTTP/1.1\r\nHost: "+socket.gethostbyname(name[7:])+"\r\n\r\n","utf-8"))
            message = sock.recv(size)
            response = message.decode().split("\r\n")
    for i in range(0,header_counter):
        line = response[i].split(": ")
        if line[0] == "Content-Length":
            content_length = int(line[1])
    #Print entity
    sock.send(bytes("GET / HTTP/1.1\r\nHost: "+socket.gethostbyname(name[7:])+"\r\n\r\n","utf-8"))
    message = sock.recv(content_length)
    response = message.decode().split("\r\n")
    print(message.decode())
    #for i in range(header_counter, len(response)-1):
        #print(response[i])
    sock.close()
    sys.exit(0)
