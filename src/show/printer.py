from threading import Thread
import time
import keyboard


class Printer:
    def __init__(self, updateHZ, l):
        self._thread_name = "Capture"
        self.wait_time = 1/updateHZ
        self.should_stop = False
        self.last_key_press = ''
        self.l = l

    def start(self):
        self._thread = Thread(target=self.update,
                              name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    def update(self):
        while not self.should_stop:
            start = time.time()

            if keyboard.is_pressed('F1'):
                self.last_key_press = 'F1'

            if keyboard.is_pressed('F2'):
                self.last_key_press = 'F2'

            if keyboard.is_pressed(self.l.change):
                self.last_key_press = self.l.change

            if keyboard.is_pressed(self.l.no):
                self.last_key_press = self.l.no

            if keyboard.is_pressed(self.l.ok):
                self.last_key_press = self.l.ok

            if keyboard.is_pressed(self.l.random):
                self.last_key_press = self.l.random

            if keyboard.is_pressed(self.l.drop):
                self.last_key_press = self.l.drop

            delta = time.time() - start
            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    def key(self):
        the_key = self.last_key_press
        self.last_key_press = ''
        return the_key
