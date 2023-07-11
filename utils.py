import time
import numpy as np
from threading import Thread
import keyboard

def is_key_down(key):
    return keyboard.is_pressed(key)

pressed = [False] * 256
def is_key_pressed(key):
    if is_key_down(key):
        ret = not pressed[ord(key)]
        pressed[ord(key)] = True
        return ret
    pressed[ord(key)] = False
    return False


class ButtonHandler:
    def __init__(self):
        self.flag =True
        self.range_s, self.range_e, self.range_step =0,1,0.005

    def threadStart(self):
        while self.flag:
            time.sleep(0.02)
            self.range_s += self.range_step
            self.range_e += self.range_step
            t = np.arange(self.range_s, self.range_e, self.range_step)
            ydata = np.sin(4*np.pi*t)
            self.ax.set_xdata(t-t[0])
            self.ax.set_ydata(ydata)
            

    def Start(self, event):
        self.flag =True
        t =Thread(target=self.threadStart)
        t.start()

    def Stop(self, event):
        self.flag =False

    