"""This module implements an enhanced listview widget with tabs."""

from typing import List, Dict, Callable, Optional

import curses

from widgets.label import Label
from widgets.listview_e import ListViewE
from widgets.listview_node import ListViewNode
from widgets.widget import Widget

from utils import keyboard, colors


class ListViewTabbed(Widget):
    """
    An enhanced listview widget with tabs.

    Each tab contains a different (enhanced or regular) buffer of
    items. When a tab is selected the buffer corresponding to that tab
    will be displayed
    """

    def __init__(self, stdscr: object, width: int = 20, height: int = 100) -> None:
        """
        Create the enhanced listview widget without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            width: The width of the pad. Default value is 20 characters
            height: The height of the pad representing the maximum
                    elements that can be added to the listview.
                    Default value: 100 lines
        """
        super().__init__(stdscr)

        self._tabs: Dict[str, List[ListViewNode]] = {}

        self._pad_cursor_x = 0
        self._start_item = 0
        self._cursor = 0

        self._listview = ListViewE(self._stdscr, width, height)

        self._sep_label = Label(self._stdscr, '')

        self._tab_pad = curses.newpad(1, 1000)
        self._tab_pad.scrollok(True)

    def set_size(self, lambda_x: Callable[[int], int], lambda_y: Callable[[int], int], lambda_w: Callable[[int], int], lambda_h: Callable[[int], int]) -> None:  # type: ignore[override]
        """
        Specify the responsive size of the window with lambda functions.

        Args:
            lambda_x: A lambda function defining the upper left
                      corner's x coordinate with the width of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
            lambda_y: A lambda function defining the upper left
                      corner's y coordinate with the height of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
            lambda_w: A lambda function defining the bottom right
                      corner's x coordinate with the width of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
            lambda_h: A lambda function defining the bottom right
                      corner's y coordinate with the height of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
        """
        super().set_size(lambda_x, lambda_y, lambda_w, lambda_h)

        self._listview.set_size(self._lambda_x, lambda y: self._lambda_y(y) + 2, self._lambda_w, lambda h: self._lambda_h(h) - 2)  # type: ignore[misc]
        self._sep_label.set_size(lambda x: self._lambda_x(x) - 1, lambda _: 2, None, None)

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super()._getxy()
        ly = self._lambda_y(y)
        lx = self._lambda_x(x)

        sy, sx = self._stdscr.getbegyx()
        colors.colored_addstr(self._stdscr, lx, ly, '<')
        colors.colored_addstr(self._stdscr, self._lambda_w(x) + lx, ly, '>')  # type: ignore[misc]

        for x_plc in (lx + 1, self._lambda_w(x)):  # type: ignore[misc]
            colors.colored_addstr(self._stdscr, x_plc, ly - 1, '┬')
            colors.colored_addstr(self._stdscr, x_plc, ly, '│')

        colors.colored_addstr(self._stdscr, lx - 1, ly + 1, f'├─┴{"─" * (self._lambda_w(x) - 3)}┴─┤')  # type: ignore[misc]
        self._stdscr.refresh()

        x_pos = 0
        for i, tab in enumerate(self._tabs.keys()):
            color = ''
            reset = ''
            sep = ''
            if i == self._cursor:
                color = '\x1b[47m\x1b[30m'
                reset = '\x1b[0m'
            if i < len(self._tabs.keys()) - 1:
                sep = '|'
            colors.colored_addstr(self._tab_pad, x_pos, 0, f'{color} {tab} {reset}{sep}')
            x_pos += len(tab) + 3

        self._listview.resize(x, y)

        self._calculate_pad_scroll()
        self._tab_pad.refresh(0, self._pad_cursor_x, sy+ly, sx+lx+2, sy+ly, sx+lx+self._lambda_w(x)-4)  # type: ignore[misc] # noqa: E226

        # If there are no tabs, return
        if not self._tabs:
            return

        self._listview.set_buffer(self._tabs[list(self._tabs.keys())[self._cursor]])

    # def horizontal_scroll(self, x: int) -> None:
    #    items_till_cursor = tuple(self.tabs.keys())[self.start_item:self._cursor + 1]
    #    if sum(map(len, items_till_cursor)) + len(items_till_cursor) * 3 >= self.lambda_w(x):
    #        self.pad_cursor_x += len(items_till_cursor[0]) + 3
    #        self.start_item += 1
    #        self.horizontal_scroll(x)

    def _calculate_pad_scroll(self) -> None:
        items_till_cursor = tuple(self._tabs.keys())[:self._cursor]
        self._pad_cursor_x = sum(map(len, items_till_cursor)) + len(items_till_cursor) * 3

    def input(self, key: int) -> Optional[str]:
        """
        Interpreters given keystrokes.

        Args:
            key: The pressed key's value

        Returns:
            Optional[str]: Returns the selected item or None if
                           nothing was selected (e.g. KEY_DOWN
                           was pressed or parent node expanded)
        """
        if key == keyboard.KEY_TAB:
            # Next tab
            if self._cursor < len(self._tabs.keys()) - 1:
                self._cursor += 1
            else:
                self._cursor = 0
        elif key == keyboard.KEY_SHIFT_TAB:
            # Previous tab
            if self._cursor > 0:
                self._cursor -= 1
            else:
                self._cursor = len(self._tabs.keys()) - 1
        elif key == curses.KEY_MOUSE:
            x, y = self._getxy()
            sy, sx = self._stdscr.getbegyx()
            mouse_event = curses.getmouse()
            if self._lambda_y(y) + sy == mouse_event[2]:
                # Previous tab
                if sx + 1 == mouse_event[1]:
                    if self._cursor > 0:
                        self._cursor -= 1
                        self._calculate_pad_scroll()
                        self._listview.set_cursor(0)
                        self.draw()
                # Next tab
                elif self._lambda_w(x) + sx + 1 == mouse_event[1]:  # type: ignore[misc]
                    if self._cursor < len(self._tabs.keys()) - 1:
                        self._cursor += 1
                        self._calculate_pad_scroll()
                        self._listview.set_cursor(0)
                        self.draw()
                # Select tab with mouse
                elif sx + 1 < mouse_event[1] < self._lambda_w(x) + sx + 1:  # type: ignore[misc]
                    pass

            return self._listview.input(key)
        else:
            return self._listview.input(key)

        # Reset the cursor of the listview
        self._listview.set_cursor(0)
        self.draw()
        return None
