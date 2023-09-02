"""This module implements a listview widget with curses."""

from typing import Tuple, List, Optional, Any
import curses

from widgets import widget
from utils import keyboard, colors


class ListView(widget.Widget):
    """A scrollable listview widget with selectable elements."""

    def __init__(self, stdscr: object, width: int = 20, height: int = 100):
        """
        Create the listview without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            width: The width of the pad
            height: The height of the pad representing the maximum
                    elements that can be added to the listview
        """
        super().__init__(stdscr)

        self._buffer: List[str] = []

        self._pad_pos_x = 0
        self._pad_pos_y = 0

        self._cursor = 0
        self._cursor_border = height

        self._width = width
        self._height = height

        self._pad = curses.newpad(height, width)
        self._pad.scrollok(True)

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super()._getxy()
        ly = self._lambda_y(y)
        lx = self._lambda_x(x)
        sy, sx = self._stdscr.getbegyx()

        self._pad.erase()
        self._stdscr.refresh()

        if self._buffer:
            self._draw_items()
            colors.colored_addstr(self._pad, 0, self._cursor, '>')

        self._pad.refresh(self._pad_pos_y, self._pad_pos_x, sy+ly, sx+lx, sy+ly+self._lambda_h(y), sx+lx+self._lambda_w(x))  # type: ignore[misc] # noqa: E226

    def _draw_items(self) -> None:
        for i, item in enumerate(self._buffer):
            colors.colored_addstr(self._pad, 2, i, item)

    def input(self, key: int) -> Optional[str]:
        """
        Interpreter given keystrokes.

        Args:
            key: The pressed key's value

        Returns:
            Optional[str]: Returns the selected item or None if
                           nothing was selected (e.g. KEY_DOWN
                           was pressed)
        """
        # When there are no items, return
        if not self._buffer:
            return None

        if key == curses.KEY_DOWN:
            if self._cursor >= self._cursor_border or self._cursor >= self._height:
                return None
            self._cursor += 1
            self.draw()
        elif key == curses.KEY_UP:
            if self._cursor == 0:
                return None
            self._cursor -= 1
            self.draw()
        elif key == keyboard.KEY_ENTER:
            return self._selected_item()
        elif key == curses.KEY_MOUSE:
            x, y = self._getxy()
            mouse_event = curses.getmouse()
            if self._lambda_x(x) <= mouse_event[1] and self._lambda_x(x) + self._lambda_w(x) >= mouse_event[1]:  # type: ignore[misc]
                if self._lambda_y(y) <= mouse_event[2] and self._lambda_y(y) + self._lambda_h(y) >= mouse_event[2]:  # type: ignore[misc]
                    return self._handle_mouse_input(mouse_event, x, y)
        return None

    def _selected_item(self) -> Optional[str]:
        return self._buffer[self._cursor]

    def _handle_mouse_input(self, mouse_event: Tuple[int, int, int, int, Any], _: int, y: int) -> Optional[str]:
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            try:
                return self._buffer[self._pad_pos_y + mouse_event[2] - self._lambda_y(y) - 1]
            except IndexError:
                pass
        return None

    def add_new(self, name: str) -> None:
        """
        Add a new item in the listview without updating the it.

        Args:
            name: The new item
        """
        self._buffer.append(name)

    def set_buffer(self, buff: List[str]) -> None:
        """
        Display the provided list of items.

        Args:
            buff: The new buffer which is going to be displayed
        """
        self._buffer = buff
        self._cursor_border = len(self._buffer) - 1
        self.draw()

    def set_cursor(self, new_pos: int) -> None:
        """
        Set the cursor of the listview to new_pos.

        Args:
            new_pos: The new y position for the cursor
        """
        self._cursor = new_pos
