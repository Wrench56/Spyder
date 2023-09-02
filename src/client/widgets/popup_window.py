"""
This module implements a popup window.

The popup window won't erase the content below it, as it creates
a new curses window.
"""

import curses
import textwrap
from typing import List, Optional, Tuple

from utils import colors, keyboard
from widgets.multiline_label import MultilineLabel


class PopUp():
    """
    A popup window with a title, message and maximum 3 menus.

    The popup can block the main program's flow. Once an action
    (menu) is selected, the action's name will be returned.
    """

    def __init__(self, stdscr: object, message: str, title: Optional[str] = None) -> None:
        """
        Create the popup window without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            message: The message displayed in the body of the popup
            title: An optional title displayed in the frame of the
                   popup
        """
        self._stdscr = stdscr
        self._title = title
        self._message = message

        self.min_width = 34
        self.max_width = 50
        self.min_height = 5
        self.max_height = 12

        self._menu_wrapping_l: str = '[ '
        self._menu_wrapping_r: str = ' ]'
        self._menu_wrapping_length = len(self._menu_wrapping_l) + len(self._menu_wrapping_r)
        self._menu_offsets: Tuple[int, int, int] = (0, 0, 0)

        self._last_x: int = 0
        self._last_y: int = 0
        self._cursor: int = 0
        self._menus: List[str] = []

        self._window = curses.newwin(1, 1, 0, 0)
        self._message_label = MultilineLabel(self._window, '')
        self._message_label.set_size(lambda _: 3, lambda _: 2, None, None)

    def add_menu(self, title: str) -> Optional['PopUp']:
        """
        Add a menu to the popup window.

        The menus are displayed in the bottom section of the popup.
        The layout of the menu depends on the number of menus.
        The layout is the following:
            1 menu : left
            2 menus: 1. right; 2. left
            3 menus: 1. right; 2. middle; 3. left

        Args:
            title: The name of the menu

        Returns:
            Optional[PopUp]: Returns the popup object so that it can
                             be chained.
                             e.g.: popup.add_menu('a').add_menu('b')
                             Returns None if the menu is already
                             present in the menus list or if there are
                             already 3 menus present
        """
        if title in self._menus:
            return None

        if len(self._menus) == 3:
            return None

        self._menus.append(title)
        return self

    @property
    def menu_wrapping_l(self) -> str:
        """
        The left menu wrapping string.

        The menus are wrapped with the menu_wrapping. For example:
        The menu "Ok" would look like "[ Ok ]" with the default
        menu_wrapping. The menu_wrapping_l property being the "[ " part
        """
        return self._menu_wrapping_l

    @menu_wrapping_l.setter
    def menu_wrapping_l(self, wrapping: str) -> None:
        self._menu_wrapping_l = wrapping
        self._menu_wrapping_length = len(self._menu_wrapping_l) + len(self._menu_wrapping_r)

    @property
    def menu_wrapping_r(self) -> str:
        """
        The right menu wrapping string.

        The menus are wrapped with the menu_wrapping. For example:
        The menu "Ok" would look like "[ Ok ]" with the default
        menu_wrapping. The menu_wrapping_r property being the " ]" part
        """
        return self._menu_wrapping_r

    @menu_wrapping_r.setter
    def menu_wrapping_r(self, wrapping: str) -> None:
        self._menu_wrapping_r = wrapping
        self._menu_wrapping_length = len(self._menu_wrapping_l) + len(self._menu_wrapping_r)

    def block(self) -> Optional[str]:
        """
        Block the main program's flow until a menu is selected.

        If no menus were added, any pressed key will return from the
        block.

        Returns:
            Optional[str]: Returns the selected menu or None if
                           nothing was selected (e.g. KEY_LEFT
                           was pressed)
        """
        self.draw()

        while True:
            # curses.KEY_LEFT and .KEY_RIGHT do not work with window.getch()
            key = self._stdscr.getch()
            if self._menus:
                result = self.input(key)
                if result is not None:
                    return result
            else:
                # Cleanup
                self._window.erase()
                self._window.refresh()
                return None

    def input(self, key: int) -> Optional[str]:
        """
        Interpreters given keystrokes.

        Args:
            key: The pressed key's value

        Returns:
            Optional[str]: Returns the selected menu or None if
                           nothing was selected (e.g. KEY_LEFT
                           was pressed)
        """
        if key == keyboard.KEY_ENTER:
            # Cleanup
            self._window.erase()
            self._window.refresh()
            return self._menus[self._cursor]

        if key in (curses.KEY_RIGHT, keyboard.KEY_TAB):
            if self._cursor == len(self._menus) - 1:
                self._cursor = 0
            else:
                self._cursor += 1
            self.draw()

        elif key == curses.KEY_LEFT:
            if self._cursor == 0:
                self._cursor = len(self._menus) - 1
            else:
                self._cursor -= 1
            self.draw()

        return None

    def _calc_menu_with_wrapping(self, item_index: int) -> int:
        return len(self._menus[item_index]) + self._menu_wrapping_length

    def _getxy(self) -> Tuple[int, int]:
        return self._last_x, self._last_y

    def resize(self, x: int, y: int) -> None:
        """
        Resize the popup window.

        Args:
            x: Parent window's width (bottom right corner's x)
            y: Parent window's height (bottom right corner's y)
        """
        self._last_x = x
        self._last_y = y

        self.draw()

    def draw(self) -> None:
        """Draw the widget."""
        x, y = self._getxy()

        extra_menu_height = 2 if self._menus else 0

        # Calculate longest line (from messages & menu line length)
        longest_line_length = max(len(max(self._message.split('\n'), key=len)),
                                  sum(map(len, self._menus)) + (self._menu_wrapping_length)
                                  * len(self._menus) + 1 * (len(self._menus) - 1))

        # Calculate width
        if (longest_line_length + 6) > self.min_width:
            if (longest_line_length + 6) > self.max_width:
                width = self.max_width

                # TODO:
                # Shorten the longest menu item so that it fits
                #
                # The following code snippet could not entirely solve the issue.
                # As of now, if your 3 menus are too long (or even 1 of them),
                # the menus will appear buggy, or a curses error will be thrown.
                #
                # if self.menus and menu_line_length >= longest_line_length:
                #    index = self.menus.index(max(self.menus, key=len))
                #    self.menus[index] = textwrap.shorten(self.menus[index], len(self.menus[index]) - (menu_line_length - width + 1), placeholder='*')

            else:
                width = longest_line_length + 6
        else:
            width = self.min_width

        # Thank you @far: https://stackoverflow.com/questions/1166317/python-textwrap-library-how-to-preserve-line-breaks
        # Don't try to understand this. The following line(s) take the message
        # and convert it to a list of wrapped lines with the criteriums provided.
        # textwrap.wrap() does not preserve line breaks, thus it might create
        # some "false positive" line breaks making the appeareance of the wrapped
        # message ugly.

        wrapped_list = [item for sublist in [textwrap.wrap(line,
                                                           break_long_words=False,
                                                           replace_whitespace=False,
                                                           width=width - 6,
                                                           max_lines=self.max_height - 4 - extra_menu_height)
                        for line in self._message.splitlines() if line.strip() != '']
                        for item in sublist]

        # Calculate height
        if len(wrapped_list) + 4 + extra_menu_height > self.min_height:
            height = len(wrapped_list) + 4 + extra_menu_height
        else:
            height = self.min_height

        sx = int((x - width) / 2)
        sy = int((y - height) / 2) - 3

        self._window.mvwin(sy, sx)
        self._window.resize(height, width)

        self._message_label.set_text('\n'.join(wrapped_list))
        self._message_label.resize(x, y)

        # Calculate where to put each menu item
        if len(self._menus) == 1:
            self._menu_offsets = (width - self._calc_menu_with_wrapping(0), 0, 0)
        elif len(self._menus) == 2:
            self._menu_offsets = (3, width - self._calc_menu_with_wrapping(1) - 3, 0)
        elif len(self._menus) == 3:
            end = width - self._calc_menu_with_wrapping(2) - 3
            start_end_distance = end - (3 + len(self._menus[0]) + self._menu_wrapping_length)

            self._menu_offsets = (3, 3 + self._calc_menu_with_wrapping(0) + int((start_end_distance - self._calc_menu_with_wrapping(1)) / 2), end)

        for i, item in enumerate(self._menus):
            if self._cursor == i:
                string = f'\x1b[47m\x1b[30m{self._menu_wrapping_l}{item}{self._menu_wrapping_r}\x1b[0m'
            else:
                string = f'{self._menu_wrapping_l}{item}{self._menu_wrapping_r}'
            colors.colored_addstr(self._window, self._menu_offsets[i], height - 3, string)

        self._window.box()
        if self._title:
            colors.colored_addstr(self._window, 2, 0, f' {self._title} ')

        self._window.refresh()
