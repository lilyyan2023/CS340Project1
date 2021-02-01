import socket
import sys


input = str(sys.argv[1])

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
            print('https given\n',file=sys.stderr)
            sys.exit(5)
        print('Not http protocol\n',file=sys.stderr)
        sys.exit(1)
    else:
        message = ""
        sock = socket.socket()
        sock.connect((socket.gethostbyname(addr),port))
        sock.sendall(bytes("GET /"+content+ " HTTP/1.1\r\nHost: "+addr+"\r\n\r\n","utf-8"))
        while(message == "" or "\r\n\r\n" not in message):
            response = sock.recv(1024)
            message += response.decode('utf-8', 'replace')
        content_length = -1
        lst = message.split("\r\n\r\n")[0].split("\r\n")
        for i in range(0,len(lst)):
            line = lst[i].split(": ")
            if line[0] == "Content-Length":
                content_length = int(line[1])
            if line[0] == "Content-Type":
                if line[1].split("; ")[0] != "text/html":
                    print("not text html\n",file=sys.stderr)
                    sys.exit(3)
        header_length = len(message.split("\r\n\r\n")[0])
        if(content_length != -1):
            while( len(message.encode()) < content_length+header_length+len("\r\n\r\n")):
                size = content_length+header_length+len("\r\n\r\n")-len(message.encode())
                if(size > 1024):
                    size = 1024
                response = sock.recv(size)
                message += response.decode('utf-8', 'replace')
        else:
            response = sock.recv(1024)
            while response:
                message += response.decode('utf-8', 'replace')
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
                    print("Redirected to:"+line[1]+"\n",file=sys.stderr)
        return message[header_length+len("\r\n\r\n"):], location,status
        

msg,location,status = connect(input)
redirect_counter = 0
while(location != "" and redirect_counter<10):
    redirect_counter += 1
    msg,location,status  = connect(location)
if(redirect_counter==10):
    print("redirect over 10 times\n",file=sys.stderr)
    sys.exit(10)
#print(msg,file=sys.stdout)
if(int(status) > 400):
    print(status+" Response\n",file=sys.stderr)
    sys.exit([2])
sys.exit(0)

