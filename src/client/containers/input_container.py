from utils import terminal, keyboard
from widgets import subwindow, label
from containers import base_container as bc

from events import on_resize

import math

class InputContainer(bc.BaseContainer):
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.setup()

    def setup(self):
        self.win = subwindow.Subwindow(self.stdscr)
        self.win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*6)-2, lambda h: 3)

    def handle_input(self, key):
        pass
    
    def rename(self, new_name: str):
        self.title_label.set_text(new_name)
        self.title_label.draw()
    
    def resize(self, x, y):
        self.win.resize(x, y)