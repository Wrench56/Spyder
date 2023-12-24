# flake8: noqa: E226

from typing import Dict, Tuple, Any

import curses
import logging
import math
import sys
import os
import json

import widgets
from screens import new_user, screen
from utils import art, keyboard, terminal, encryption


class Login(screen.Screen):
    def __init__(self, stdscr: object, struct: object) -> None:
        super().__init__(stdscr)
        self.struct = struct

        # Rename terminal
        terminal.rename_terminal('Spyder - Login')

        # Create widgets
        self.setup()

        # Start the logic part
        self.logic()

    def setup(self) -> None:

        # UI Infos:
        #  - Width: 65
        #  - Height: 8

        self.set_min(72, 14)
        self.username_win = widgets.Subwindow(self.stdscr)
        self.username_win.set_size(lambda x: math.floor((x-65)/2), lambda y: math.floor((y-8)/2), lambda w: 20, lambda h: 3)
        self.username_label = widgets.Label(self.username_win.get(), ' Username ')
        self.username_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.username_textbox = widgets.Textbox(self.username_win.get(), width=19, height=1)
        self.username_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)

        self.password_win = widgets.Subwindow(self.stdscr)
        self.password_win.set_size(lambda x: math.floor((x-65)/2), lambda y: math.floor((y-8)/2)+4, lambda w: 20, lambda h: 3)
        self.password_label = widgets.Label(self.password_win.get(), ' Password ')
        self.password_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.password_textbox = widgets.Textbox(self.password_win.get(), width=19, height=1, show_chars='*')
        self.password_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)

        self.logo_label = widgets.MultilineLabel(self.stdscr, art.HEADER)
        self.logo_label.set_size(lambda x: math.floor((x-65)/2)+25, lambda y: math.floor((y-8)/2)-2, None, None)
        self.motto_label = widgets.Label(self.stdscr, f'\x1b[31m{art.MOTTO}')
        self.motto_label.set_size(lambda x: math.floor((x-65)/2)+47, lambda y: math.floor((y-8)/2)+6, None, None)
        self.create_label = widgets.Label(self.stdscr, 'Or PRESS CTRL+N to create a new local user!')
        self.create_label.set_size(lambda x: math.floor((x-34)/2), lambda y: math.floor((y-8)/2)+10, None, None)

        self.resize()

    def logic(self) -> None:
        self.username_textbox.update_cursor()

        box_index: int = 0
        while True:
            ch: int = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            if ch == curses.KEY_RESIZE:
                self.resize()
                self.focus_cursor(box_index)
            elif ch == keyboard.KEY_TAB:
                box_index = (1, 0)[box_index]
                self.focus_cursor(box_index)
            elif ch == keyboard.KEY_ENTER:
                username: str = self.username_textbox.text
                password: str = self.password_textbox.text
                if not username or not password:
                    logging.critical('No username and/or password provided!')
                    curses.endwin()
                    sys.exit()

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

            elif ch == 12:  # CTRL + L, unlock/lock & update config file
                username, password = self._fetch_credentials()
                if not username or not password:
                    continue

                # Lock config
                if os.path.exists(f'data/users/{username}/config.json'):
                    self._update_config(username, password)
                    os.remove(f'data/users/{username}/config.json')
                    continue

                # Unlock config
                with open(f'data/users/{username}/secrets/config.bin',
                          'rb') as bfile:
                    config = encryption.decrypt_json(bfile.read(), self._load_login_bytes(username, password)['CONFIG_PASSWORD'])
                    bfile.close()
                with open(f'data/users/{username}/config.json',
                          'w', encoding='utf-8') as cfile:
                    cfile.write(json.dumps(config, indent=4))
                    cfile.close()
            elif ch == 21:  # CTRL + U, update config file without locking
                username, password = self._fetch_credentials()
                if not username or not password:
                    continue

                self._update_config(username, password)

            else:
                if box_index == 0:
                    self.username_textbox.input(ch)
                else:
                    self.password_textbox.input(ch)

    def _update_config(self, username: str, password: str) -> None:
        key = self._load_login_bytes(username, password)['CONFIG_PASSWORD']
        with open(f'data/users/{username}/config.json', 'r', encoding='utf-8') as cfile:
            buffer = cfile.read()
            cfile.close()
        with open(f'data/users/{username}/secrets/config.bin', 'wb') as bfile:
            bfile.write(encryption.encrypt_json(json.loads(buffer), key))
            bfile.close()

    def _load_login_bytes(self, username: str, password: str) -> Dict[Any, Any]:
        with open(f'data/users/{username}/secrets/login.bin', 'rb') as file:
            buffer = file.readlines()[10]
            file.close()
        return encryption.decrypt_json(buffer, encryption.s2k(password))

    def _fetch_credentials(self) -> Tuple[str, str]:
        username: str = self.username_textbox.text
        password: str = self.password_textbox.text
        if not username:
            logging.critical('No username provided')
        if not password:
            logging.critical('No password provided')
        if not os.path.exists(f'data/users/{username}'):
            logging.critical('No such user')

        return username, password

    def focus_cursor(self, box_index: int) -> None:
        if box_index == 0:
            self.username_textbox.update_cursor()
        else:
            self.password_textbox.update_cursor()

    def resize(self) -> None:
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
