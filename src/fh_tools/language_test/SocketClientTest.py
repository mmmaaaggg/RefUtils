from socket import socket, AF_INET, SOCK_STREAM

host = 'localhost'
port = 9876
backlog = 5
buffsize = 1024
address = (host, port)
TcpClientSock = socket(AF_INET, SOCK_STREAM)
TcpClientSock.connect(address)

data = input('> ')
if data:
    TcpClientSock.send(data)
data = TcpClientSock.recv(buffsize)
if data:
    print(data)
TcpClientSock.close()
