from screens import screen
from widgets import textbox, label, subwindow
from utils import art, colors, keyboard, terminal

import curses
import math

class Login(screen.Screen):
    def __init__(self, stdscr, struct) -> None:
        super().__init__(stdscr)
        self.struct = struct

        # Rename terminal
        terminal.rename_terminal('Spyder - Login')

        # Create widgets
        self.setup()

        # Start the logic part
        self.logic()

    def setup(self):

        # UI Infos:
        #  - Width: 65
        #  - Height: 8

        self.set_min(72, 14)

        self.username_win = subwindow.Subwindow(self.stdscr)
        self.username_win.set_size(lambda x: math.floor((x-65)/2), lambda y: math.floor((y-8)/2), lambda w: 20, lambda h: 3)
        self.username_label = label.Label(self.username_win.get(), ' Username ')
        self.username_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.username_textbox = textbox.Textbox(self.username_win.get(), width=19, height=1)
        self.username_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)

        self.password_win = subwindow.Subwindow(self.stdscr)
        self.password_win.set_size(lambda x: math.floor((x-65)/2), lambda y: math.floor((y-8)/2)+4, lambda w: 20, lambda h: 3)
        self.password_label = label.Label(self.password_win.get(), ' Password ')
        self.password_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.password_textbox = textbox.Textbox(self.password_win.get(), width=19, height=1, show_chars='*')
        self.password_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)


        self.logo_label = label.MultilineLabel(self.stdscr, art.HEADER)
        self.logo_label.set_size(lambda x: math.floor((x-65)/2)+25, lambda y: math.floor((y-8)/2)-2, None, None)
        self.motto_label = label.Label(self.stdscr, art.MOTTO, color=curses.color_pair(colors.RED_ON_BLACK))
        self.motto_label.set_size(lambda x: math.floor((x-65)/2)+47, lambda y: math.floor((y-8)/2)+6, None, None)

        y, x = self.stdscr.getmaxyx()
        if self.resize_check(x, y):
            self.resize(x, y)
    
    def logic(self):
        self.username_textbox.update_cursor()

        box_index = 0
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            elif ch == curses.KEY_RESIZE:
                y, x = self.stdscr.getmaxyx()
                if self.resize_check(x, y):
                    self.resize(x, y)
                if box_index == 0:
                    self.username_textbox.update_cursor()
                else:
                    self.password_textbox.update_cursor()
            elif ch == keyboard.KEY_TAB:
                if box_index == 0:
                    box_index = 1
                    self.password_textbox.update_cursor()
                else:
                    box_index = 0
                    self.username_textbox.update_cursor()
            elif ch == keyboard.KEY_ENTER:
                username = self.username_textbox.get_text()
                password = self.password_textbox.get_text()
                if username == '' or password == '':
                    print('We have a problem!')
                    continue
                    
                self.struct.username = username
                self.struct.password = password

                # Exit the screen
                return

            else:
                if box_index == 0:
                    self.username_textbox.input(ch)
                else:
                    self.password_textbox.input(ch)

    def resize(self, x, y):
        self.stdscr.erase()

        self.username_win.resize(x, y)
        self.username_label.resize(x, y)
        self.username_textbox.resize(x, y)

        self.password_win.resize(x, y)
        self.password_label.resize(x, y)
        self.password_textbox.resize(x, y)

        self.logo_label.resize(x, y)
        self.motto_label.resize(x, y)

        self.stdscr.refresh()        
