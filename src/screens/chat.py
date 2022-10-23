from screens import screen
from utils import terminal, keyboard
from widgets import subwindow

import curses
import math
import time

class Chat(screen.Screen):
    def __init__(self, stdscr, struct) -> None:
        super().__init__(stdscr)
        self.struct = struct

        self.state = 3

        # Rename terminal
        terminal.rename_terminal('Spyder')

        # Clear previous screen
        self.stdscr.erase()

        # Create widgets
        self.setup()

        # Start the logic part
        self.logic()

    def setup(self):
        
        self.set_min(120, 25)

        self.contacts_win = subwindow.Subwindow(self.stdscr)
        self.chat_win = subwindow.Subwindow(self.stdscr)
        self.input_win = subwindow.Subwindow(self.stdscr)

        self.special_win = subwindow.Subwindow(self.stdscr)
        self.custom_win = subwindow.Subwindow(self.stdscr)

        self.set_size()

        y, x = self.stdscr.getmaxyx()
        if self.resize_check(x, y):
            self.resize(x, y)


    def logic(self):
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            elif ch == keyboard.KEY_TAB:
                self.state += 1
                if self.state == 4:
                    self.state = 0

                self.set_size()
                y, x = self.stdscr.getmaxyx()
                curses.resize_term(y, x)
                if self.resize_check(x, y):
                    self.resize(x, y)
            elif ch == curses.KEY_RESIZE:
                y, x = self.stdscr.getmaxyx()
                curses.resize_term(y, x)
                if self.resize_check(x, y):
                    self.resize(x, y)
    
    def set_size(self):
        
        self.contacts_win.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)+1, lambda h: h-2)
        self.chat_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*6)-2, lambda h: h-5)
        self.input_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*6)-2, lambda h: 3)
        
        if self.state >= 2:
            self.chat_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*4)-2, lambda h: h-5)
            self.input_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*4)-2, lambda h: 3)
            self.custom_win.set_size(lambda x: math.floor((x/8)*6), lambda y: 1, lambda w: math.floor((w/8)*2), lambda h: h-2)

        if self.state == 1 or self.state == 3:
            self.contacts_win.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)+1, lambda h: math.floor((h/3)*2))
            self.special_win.set_size(lambda x: 1, lambda y: math.floor((y/3)*2)+1, lambda w: math.floor((w/8)*2)+1, lambda h: math.ceil(h/3)-2)

    def resize(self, x, y):
        # Prevents curses.error on rapid resizing (not 100% efficiency)
        time.sleep(0.1) 
        curses.endwin()
        # ============== #

        self.stdscr.erase()

        self.contacts_win.resize(x, y)
        self.chat_win.resize(x, y)
        self.input_win.resize(x, y)
        if self.state >= 2:
            self.custom_win.resize(x, y)
        if self.state == 1 or self.state == 3:
            self.special_win.resize(x, y)

        self.stdscr.refresh()