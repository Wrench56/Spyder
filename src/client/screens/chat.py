# flake8: noqa: E226

import curses
import math
import logging

from screens import screen
from utils import terminal
from widgets import subwindow, listview_tabbed

from events import on_resize


class Chat(screen.Screen):
    def __init__(self, stdscr: object) -> None:
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

    def setup(self) -> None:
        on_resize.subscribe(self.resize)
        self.set_min(120, 25)

        self.channel_win = subwindow.Subwindow(self.stdscr, True)
        self.channel_lv = listview_tabbed.ListViewTabbed(self.channel_win.get(), width=200, height=10000)
        self.chat_win = subwindow.Subwindow(self.stdscr, True)
        self.info_win = subwindow.Subwindow(self.stdscr, True)
        self.input_win = subwindow.Subwindow(self.stdscr, True)
        self.special_win = subwindow.Subwindow(self.stdscr, True)

        self.set_size()

    def logic(self) -> None:
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            if ch == ord('s'):
                self.state += 1
                if self.state == 4:
                    self.state = 0
                self.set_size()
                y, x = self.stdscr.getmaxyx()
                curses.resize_term(y, x)
                if self.resize_check(x, y):
                    on_resize.trigger(x, y)
            elif ch == curses.KEY_RESIZE:
                self.stdscr.erase()
                y, x = self.stdscr.getmaxyx()
                curses.resize_term(y, x)
                if self.resize_check(x, y):
                    on_resize.trigger(x, y)
            else:
                logging.debug(self.channel_lv.input(ch))

    def set_size(self) -> None:

        self.channel_win.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)+1, lambda h: h-2)
        self.channel_lv.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)-2, lambda h: h-5)
        self.chat_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*6)-2, lambda h: h-5)
        self.input_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*6)-2, lambda h: 3)

        if self.state >= 2:
            self.chat_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: 1, lambda w: math.floor((w/8)*4)-2, lambda h: h-5)
            self.input_win.set_size(lambda x: math.floor((x/8)*2)+2, lambda y: y-4, lambda w: math.floor((w/8)*4)-2, lambda h: 3)
            self.special_win.set_size(lambda x: (math.floor((x/8)*2)+2+math.floor((x/8)*4)-2), lambda y: 1, lambda w: math.ceil((w/8)*2)-1, lambda h: h-2)

        if self.state in (1, 3):
            self.channel_win.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)+1, lambda h: math.floor((h/3)*2))
            self.channel_lv.set_size(lambda x: 1, lambda y: 1, lambda w: math.floor((w/8)*2)-2, lambda h: math.floor((h/3)*2)-3)
            self.info_win.set_size(lambda x: 1, lambda y: math.floor((y/3)*2)+1, lambda w: math.floor((w/8)*2)+1, lambda h: math.ceil(h/3)-2)

        y, x = self.stdscr.getmaxyx()
        curses.resize_term(y, x)
        if self.resize_check(x, y):
            on_resize.trigger(x, y)

    def resize(self, x: int, y: int) -> None:
        self.stdscr.erase()
        self.stdscr.refresh()

        self.channel_win.get().erase()
        self.channel_win.resize(x, y)
        self.chat_win.get().erase()
        self.chat_win.resize(x, y)
        self.input_win.get().erase()
        self.input_win.resize(x, y)
        if self.state >= 2:
            self.special_win.get().erase()
            self.special_win.resize(x, y)
        if self.state in (1, 3):
            self.info_win.get().erase()
            self.info_win.resize(x, y)

        self.channel_lv.resize(x, y)
