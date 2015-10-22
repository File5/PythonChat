import threading
import socket
from sys import stdout, stdin

class ChatServer:

    def __init__(self):
        self.clients = set()
        self.clients_lock = threading.Lock()
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 1488
        self.read_settings()

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(10)
        self.th = []

        print("Chat server started on", self.HOST)
        while True:
            client, address = self.s.accept()
            self.th.append(threading.Thread(target=self.listener,
                                            args = (client,address)).start())
        s.close()

    def read_settings(self):
        #  reading settings.ctg and setting variables
        try:
            with open('settings.cfg') as f:
                headers = {'host': 'Server-Host:',
                           'port': 'Server-Port:'}
                for line in f:
                    if line.startswith(headers['host']):
                        self.HOST = line[ len(headers['host']) : ].strip()
                    elif line.startswith(headers['port']):
                        self.PORT = int(line[ len(headers['port']) : ].strip())
        except FileNotFoundError:
            pass

    def listener(self, client, address):
        print(address[0], ": connected.")
        with self.clients_lock:
            self.clients.add(client)
        try:
            while True:
                data = client.recv(1024)
                if data == b'':
                    pass
                else:
                    data = str(data, "cp1251")
                    print(address[0], ":", data, end='')
                    if data.strip().startswith('/'):
                        data = data[ data.find('/', 1) : ]
                        if data.startswith('/clients'):
                            client.send(self.get_clients_list())
                        continue
                    with self.clients_lock:
                        to_remove = []
                        for c in self.clients:
                            try:
                                c.sendall(bytes(data, "cp1251"))
                            except Exception:
                                print(address[0], ": error while sending data")
                        for c in to_remove:
                            self.clients.remove(c)
        except Exception as e:
            print(address[0], ": disconnected.")
            with self.clients_lock:
                self.clients.remove(client)
        finally:
            client.close()

    def get_clients_list(self):
        addrs = map(socket.socket.getpeername, self.clients)
        addrs = [x[0] for x in addrs]
        return bytes('===Clients===\n' + '\n'.join(addrs) + '\n', "cp1251")

if __name__ == "__main__":
    server = ChatServer()


