import socket
import sys


input = str(sys.argv[1])
output = sys.stdout
errMsg = sys.stderr

def connect(name):
    content = ""
    lst = name.split("/")
    for i in range(3,len(lst)):
        content+= lst[i]
        if(i < len(lst)-1):
            content+="/"
    addr = lst[2]

    if name[0:7] != "http://":
        errMsg.write('error')
        sys.exit(1)
    else:
        message = ""
        sock = socket.socket()
        sock.connect((socket.gethostbyname(addr),80))
        sock.sendall(bytes("GET /"+content+ " HTTP/1.1\r\nHost: "+addr+"\r\n\r\n","utf-8"))
        while(message == "" or "\r\n\r\n" not in message):
            response = sock.recv(1024)
            message += response.decode()
        content_length = -1
        lst = message.split("\r\n\r\n")[0].split("\r\n")
        for i in range(0,len(lst)):
            line = lst[i].split(": ")
            if line[0] == "Content-Length":
                content_length = int(line[1])
        header_length = len(message.split("\r\n\r\n")[0])
        while( len(message) < content_length+header_length+len("\r\n\r\n")):
            size = content_length+header_length+len("\r\n\r\n")-len(message)
            if(size > 1024):
                size = 1024
            response = sock.recv(size)
            message += response.decode()
        #response = sock.recv(header_length+len("\r\n\r\n"))
        #message += response.decode()
        location = ""
        status = message[9:12]
        if(status == "301" or status == "302"):
            for i in range(0,len(lst)):
                line = lst[i].split(": ")
                if line[0] == "Location":
                    location = line[1]
        return message[header_length+len("\r\n\r\n"):], location,status 
        

msg,location,status = connect(input)
redirect_counter = 0
while(location != "" and redirect_counter<10):
    redirect_counter += 1
    msg,location,status  = connect(location)
if(redirect_counter==10):
    errMsg.write("redirect over 10 times")
    sys.exit(10)
output.write(msg)
if(int(status) > 400):
    sys.exit(2)
sys.exit(0)

