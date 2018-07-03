from socket import *
from time import ctime

host = 'localhost'
port = 5301
backlog = 5
buffsize = 1024
address = (host, port)
TcpSerSock = socket(AF_INET, SOCK_STREAM)
TcpSerSock.bind(address)
TcpSerSock.listen(backlog)
try:
    while True:
        print('waiting for connecting...')
        tcpCliSock, addr = TcpSerSock.accept()
        print('connected from:', addr)
        while True:
            data = tcpCliSock.recv(buffsize)
            print('receive: ', data)
            if not data:
                break
            tcpCliSock.send('[%s] %s' % (ctime(), data))
        tcpCliSock.close()
    TcpSerSock.close()
except EOFError:
    print('connect closed E')
except KeyboardInterrupt:
    print('connect closed I')
