from tkinter import *
from socket import gethostname, gethostbyname
import socketutils

class ChatApplication:
    
    def __init__(self):
        #  creating widgets
        self.root = Tk()
        self.root.geometry("600x450")
        self.root.title("Chat")
        self.root.bind('<Return>', self.send_msg)
        
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.text = Text(self.root, yscrollcommand=self.scrollbar.set)
        self.text['state'] = DISABLED
        self.text['height'] = 1
        self.text.pack(fill=BOTH, expand=1)
        
        self.scrollbar.config(command=self.text.yview)
        
        self.send_frame = Frame(self.root)
        self.send_frame.pack(side=BOTTOM, fill=X)
        
        self.edit = Entry(self.send_frame)
        self.edit.pack(side=LEFT, expand=1, fill=X)

        self.button = Button(self.send_frame, text="Send", command=self.send_msg)
        self.button.pack(side=RIGHT)

        #  setting up receiving and sending sockets
        self.name = gethostbyname(gethostname())
        self.THISHOST = gethostbyname(gethostname())
        self.HOST = '127.0.0.1'
        self.PORT = 1489
        self.read_settings()

        self.client = socketutils.ClientSocketListener(self.print_msg, self.HOST, self.PORT)

        #  setting available commands
        self.available = {'/font': self.set_font,
                          '/bg': self.set_bg,
                          '/color': self.set_fg,
                          '/matrix': self.matrix,
                          '/clear': self.clear_text,
                          '/help': self.print_help,
                          '/name': self.set_name,
                          }
        
        self.root.mainloop()
    
    def print_msg(self, msg):
        msg = str(msg, "cp1251")
        self.text['state'] = NORMAL
        self.text.insert(END, msg)
        self.text.see(END)
        self.text['state'] = DISABLED
    
    def send_msg(self, *args):
        text = self.edit.get()
        if text == '':
            return
        data = self.name + ': ' + text + '\n'
        if text.startswith('/'):
            self.print_msg(bytes(data, "cp1251"))
            self.run_command(text)
            data = '/' + data
        self.client.send(bytes(data, "cp1251"))
        self.edit.delete(0, END)

    def read_settings(self):
        #  reading settings.ctg and setting variables
        try:
            with open('settings.cfg') as f:
                headers = {'name': 'Name: ',
                           'thishost': "This-Host: ",
                           'host': 'Server-Host: ',
                           'port': 'Server-Port: '}
                for line in f:
                    if line.startswith(headers['name']):
                        self.name = line[ len(headers['name']) : ].strip()
                    elif line.startswith(headers['thishost']):
                        self.THISHOST = line[ len(headers['thishost']) : ].strip()
                    elif line.startswith(headers['host']):
                        self.HOST = line[ len(headers['host']) : ].strip()
                    elif line.startswith(headers['port']):
                        self.PORT = int(line[ len(headers['port']) : ].strip())
        except FileNotFoundError:
            pass

    def run_command(self, text):
        for command in self.available:
            if text.startswith(command):
                self.available[command]( text[ len(command) : ].strip() )

    def set_font(self, x):
        self.text['font'] = x
        self.edit['font'] = x
        
    def set_bg(self, x):
        self.text['bg'] = x
        self.edit['bg'] = x
        
    def set_fg(self, x):
        self.text['fg'] = x
        self.edit['fg'] = x

    def matrix(self, *args):
        self.text['font'] = "Consolas 12"
        self.edit['font'] = "Consolas 12"
        self.text['bg'] = "black"
        self.edit['bg'] = "black"
        self.text['fg'] = "#00aa00"
        self.edit['fg'] = "#00aa00"

    def clear_text(self, *args):
        self.text['state'] = NORMAL
        self.text.delete(1.0, END)
        self.text.see(END)
        self.text['state'] = DISABLED

    def print_help(self, *args):
        helptext = '\n'.join(self.available) + '\n'
        self.print_msg(bytes(helptext, "cp1251"))

    def set_name(self, name):
        self.name = name
        self.print_msg(bytes(name + ": name saved.\n", "cp1251"))

if __name__ == "__main__":
    application = ChatApplication()
