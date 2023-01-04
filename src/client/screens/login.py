from screens import screen, new_user
from widgets import textbox, label, subwindow
from utils import art, keyboard, terminal

import curses
import math
import logging


class Login(screen.Screen):
    def __init__(self, stdscr: curses.window, struct: object) -> None:
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
        self.motto_label = label.Label(self.stdscr, f'\x1b[31m{art.MOTTO}')
        self.motto_label.set_size(lambda x: math.floor((x-65)/2)+47, lambda y: math.floor((y-8)/2)+6, None, None)
        self.create_label = label.Label(self.stdscr, 'Or PRESS CTRL+N to create a new local user!')
        self.create_label.set_size(lambda x: math.floor((x-34)/2), lambda y: math.floor((y-8)/2)+10, None, None)

        self.resize()

    def logic(self):
        self.username_textbox.update_cursor()

        box_index: int = 0
        while True:
            ch: int = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            elif ch == curses.KEY_RESIZE:
                self.resize()
                self.focus_cursor(box_index)
            elif ch == keyboard.KEY_TAB:
                box_index = (1, 0)[box_index]
                self.focus_cursor(box_index)
            elif ch == keyboard.KEY_ENTER:
                username: str = self.username_textbox.get_text()
                password: str = self.password_textbox.get_text()
                if username == '' or password == '':
                    logging.critical('No username and/or password provided!')
                    curses.endwin()
                    quit()

                self.struct.username = username
                self.struct.password = password

                # Exit this screen
                return
            elif ch == 14:  # CTRL + N, create new user
                new_user.NewUser(self.stdscr)
                # After NewUser() is done:

                self.resize()
                self.username_textbox.draw()
                self.password_textbox.draw()
                self.focus_cursor(box_index)

            else:
                if box_index == 0:
                    self.username_textbox.input(ch)
                else:
                    self.password_textbox.input(ch)

    def focus_cursor(self, box_index):
        if box_index == 0:
            self.username_textbox.update_cursor()
        else:
            self.password_textbox.update_cursor()

    def resize(self):
        y, x = self.stdscr.getmaxyx()
        if not self.resize_check(x, y):
            return

        self.stdscr.erase()
        self.stdscr.refresh()

        self.username_win.resize(x, y)
        self.username_label.resize(x, y)
        self.username_textbox.resize(x, y)

        self.password_win.resize(x, y)
        self.password_label.resize(x, y)
        self.password_textbox.resize(x, y)

        self.logo_label.resize(x, y)
        self.motto_label.resize(x, y)
        self.create_label.resize(x, y)
