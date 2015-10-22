from threading import Thread
from time import sleep

class SpamMachine(Thread):
    def __init__(self, text, func, sleep_time=0.1):
        Thread.__init__(self)
        self.text = text
        self.func = func
        self.sleep_time = sleep_time
        self.is_run = True
        
    def set_text(self, text):
        self.text = text
        
    def run(self):
        self.is_run = True
        while self.is_run:
            self.func(self.text)
            sleep(self.sleep_time)
            
    def stop(self):
        self.is_run = False
