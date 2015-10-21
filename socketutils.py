import socket
from threading import Thread

class ClientSocketListener(Thread):

    def __init__(self, update, HOST='127.0.0.1', PORT=1488):
        Thread.__init__(self)
        self.update = update
        self.HOST = HOST
        self.PORT = PORT
        self.is_run = True

        self.s = socket.socket()
        self.s.connect((self.HOST, self.PORT))

        self.start()

    def send(self, data):
        self.s.send(data)

    def run(self, *args):
        while self.is_run:
            try:
                data = self.s.recv(1024)
                if data != b'':
                    self.update(data)
            except Exception as e:
                break
    
    def close(self):
        self.is_run = False
        self.s.close()
