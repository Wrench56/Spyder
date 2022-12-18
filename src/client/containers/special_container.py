from utils import terminal, keyboard
from widgets import subwindow, label
from containers import base_container as bc

from events import on_resize

import math

class SpecialContainer(bc.BaseContainer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        
    def setup(self):
        self.win = subwindow.Subwindow(self.stdscr)
        self.win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*6)-2, lambda h: h-5)

        self.title_label = label.Label(self.win.get(), ' Title ')
        self.title_label.set_size(lambda x: 3, lambda y: 0, None, None)

    def handle_input(self, key):
        pass