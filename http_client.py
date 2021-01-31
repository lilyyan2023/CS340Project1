import socket
import sys


input = str(sys.argv[1])
output = sys.stdout
errMsg = sys.stderr

def connect(name):
    content = ""
    port = 80
    lst = name.split("/")
    addr = ""
    for i in range(3,len(lst)):
        content+= lst[i]
        if(i < len(lst)-1):
            content+="/"
    addr = lst[2]
    if ":" in lst[2]:
        port = int(lst[2][lst[2].index(":")+1:])
        addr = lst[2][0:lst[2].index(":")]

    if name[0:7] != "http://":
        if name[0:8] == "https://":
            errMsg.write('https given')
            sys.exit(5)
        errMsg.write('Not http protocol')
        sys.exit(1)
    else:
        message = ""
        sock = socket.socket()
        sock.connect((socket.gethostbyname(addr),port))
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
            if line[0] == "Content-Type":
                if line[1].split("; ")[0] != "text/html":
                    errMsg.write("not text html")
                    sys.exit(3)
        header_length = len(message.split("\r\n\r\n")[0])
        if(content_length != -1):
            while( len(message.encode()) < content_length+header_length+len("\r\n\r\n")):
                size = content_length+header_length+len("\r\n\r\n")-len(message.encode())
                if(size > 1024):
                    size = 1024
                response = sock.recv(size)
                message += response.decode()
        else:
            response = sock.recv(1024)
            while response:
                message += response.decode()
                response = sock.recv(1024)
        #response = sock.recv(header_length+len("\r\n\r\n"))
        #message += response.decode()
        location = ""
        status = message[9:12]
        if(status == "301" or status == "302"):
            for i in range(0,len(lst)):
                line = lst[i].split(": ")
                if line[0] == "Location":
                    location = line[1]
                    errMsg.write("Redirected to:"+line[1])
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
    errMsg.write(status+" Response")
    sys.exit(2)
sys.exit(0)

