from screens import screen
from utils import terminal, keyboard
from widgets import subwindow, listview, label, textbox

from events import on_resize

import curses
import math
import time

class Chat(screen.Screen):
    def __init__(self, stdscr) -> None:
        super().__init__(stdscr)

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
        on_resize.subscribe(self.resize)
        self.set_min(120, 25)

        self.channel_win = subwindow.Subwindow(self.stdscr, True)
        self.channel_lv = listview.ListView(self.channel_win.get(), width=200, height=10000)
        self.chat_win = subwindow.Subwindow(self.stdscr, True)
        self.info_win = subwindow.Subwindow(self.stdscr, True)
        self.input_win = subwindow.Subwindow(self.stdscr, True)
        self.special_win = subwindow.Subwindow(self.stdscr, True)


        self.set_size()

    def logic(self):
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            elif ch == keyboard.KEY_TAB:
                self.state += 1
                if self.state == 4:
                    self.state = 0
            elif ch == curses.KEY_RESIZE:
                y, x = self.stdscr.getmaxyx()
                curses.resize_term(y, x)
                if self.resize_check(x, y):
                    on_resize.trigger(x, y)
            else:
                print(self.channel_lv.input(ch))
    
    def set_size(self):
        
        self.channel_win.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)+1, lambda h: h-2)
        self.channel_lv.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)-2, lambda h: h-5)
        self.chat_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*6)-2, lambda h: h-5)
        self.input_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*6)-2, lambda h: 3)

        if self.state >= 2:
            self.chat_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*4)-2, lambda h: h-5)
            self.input_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*4)-2, lambda h: 3)
            self.special_win.set_size(lambda x: (math.floor((x/8)*2)+2+math.floor((x/8)*4)-2), lambda y: 1, lambda w: math.ceil((w/8)*2)-1, lambda h: h-2)

        if self.state == 1 or self.state == 3:
            self.channel_win.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)+1, lambda h: math.floor((h/3)*2))
            self.channel_lv.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)-2, lambda h: math.floor((h/3)*2)-3)
            self.info_win.set_size(lambda x: 1, lambda y: math.floor((y/3)*2)+1, lambda w: math.floor((w/8)*2)+1, lambda h: math.ceil(h/3)-2)
            
        

        y, x = self.stdscr.getmaxyx()
        curses.resize_term(y, x)
        if self.resize_check(x, y):
            on_resize.trigger(x, y)

    def resize(self, x, y):
        time.sleep(0.01)
        self.stdscr.erase()
        
        self.channel_win.resize(x, y)
        self.chat_win.resize(x, y)
        self.input_win.resize(x, y)
        if self.state >= 2:
            self.special_win.resize(x, y)
        if self.state == 1 or self.state == 3:
            self.info_win.resize(x, y)
        self.stdscr.refresh()

        self.channel_lv.resize(x, y)

        self.stdscr.refresh()