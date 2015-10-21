from socketutils import ClientSocketListener
from sys import stdout, stdin
import socket

##s = SendSocket('192.168.1.10', 1489)
##while True:
##    data = input("Data: ")
##    try:
##        s.send(data + '\n')
##        print(s.s.recv(1024))
##    except Exception as e:
##        print(e)
##s = socket.socket()
##s.connect(('192.168.1.10', 1488))
##s.send(b'')
##while True:
##    data = input("Data: ")
##    try:
##        s.send(bytes(data + '\n', "cp1251"))
##        data = b''
##        while data == b'':
##            data = s.recv(1024)
##        print(data)
##    except Exception as e:
##        print(e)
client = ClientSocketListener(lambda x: print(str(x, "cp1251")), '192.168.1.10', 1488)
while True:
    stdout.flush()
    data = input() + '\n'
    stdin.flush()
    client.send(bytes(data, "cp1251"))
