import socket
from threading import Thread

class ClientSocketListener:

    def __init__(self, update, HOST='127.0.0.1', PORT=1488):
        self.update = update
        self.HOST = HOST
        self.PORT = PORT

        self.s = socket.socket()
        self.s.connect((self.HOST, self.PORT))

        self.th = Thread(target=self.listen, args=(self,))
        self.th.start()

    def send(self, data):
        self.s.send(data)

    def listen(self, *args):
        while True:
            try:
                data = b''
                while data == b'':
                    data = self.s.recv(1024)
                    self.update(data)
            except Exception as e:
                print(e)
                break
