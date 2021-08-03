# PythonChat
Simple GUI chat

I'm just trying to use sockets and understanding how they work.

## Usage

1. Edit `settings.cfg` accordingly
2. Start server
```
python3 chatserver.py
```
3. Start clients
```
python3 chat.py
```

![image](https://user-images.githubusercontent.com/14141957/128044137-80b35c83-9336-4eb1-a327-07ffe930ebb7.png)

Server stdout log:
```
$ python3 chatserver.py
Chat server started on 192.168.0.101
192.168.0.101 : connected.
192.168.0.101 : connected.
192.168.0.101 : User1: Hello
192.168.0.101 : User2: Hello, my friend!
192.168.0.101 : User1: How are you doing?
192.168.0.101 : /User1: /clients
```
