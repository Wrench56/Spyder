from utils import terminal, keyboard
from widgets import subwindow, label
from containers import base_container as bc

from events import on_resize

import math

class ChatContainer(bc.BaseContainer):
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.setup()

    def setup(self):
        self.win = subwindow.Subwindow(self.stdscr)
        self.win.set_size(lambda x: 0, lambda y: 0, lambda w: 1, lambda h: 1)

        self.title_label = label.Label(self.win.get(), ' Title ')
        self.title_label.set_size(lambda x: 3, lambda y: 0, None, None)

    def handle_input(self, key):
        pass
    
    def rename(self, new_name: str):
        self.title_label.set_text(new_name)
        self.title_label.draw()
    
    def resize(self, x, y):
        self.win.resize(x, y)
        self.title_label.resize(x, y)