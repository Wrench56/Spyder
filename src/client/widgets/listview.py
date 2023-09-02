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

        self.buffer: List[str] = []

        self.pad_pos_x = 0
        self.pad_pos_y = 0

        self.cursor = 0
        self.cursor_border = height

        self.width = width
        self.height = height

        self.pad = curses.newpad(height, width)
        self.pad.scrollok(True)

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super().getxy()
        ly = self.lambda_y(y)
        lx = self.lambda_x(x)
        sy, sx = self.stdscr.getbegyx()

        self.pad.erase()
        self.stdscr.refresh()

        if self.buffer:
            self.draw_items()
            colors.colored_addstr(self.pad, 0, self.cursor, '>')

        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, sy+ly, sx+lx, sy+ly+self.lambda_h(y), sx+lx+self.lambda_w(x))  # type: ignore[misc] # noqa: E226

    def draw_items(self) -> None:
        for i, item in enumerate(self.buffer):
            colors.colored_addstr(self.pad, 2, i, item)

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
        if not self.buffer:
            return None

        if key == curses.KEY_DOWN:
            if self.cursor >= self.cursor_border or self.cursor >= self.height:
                return None
            self.cursor += 1
            self.draw()
        elif key == curses.KEY_UP:
            if self.cursor == 0:
                return None
            self.cursor -= 1
            self.draw()
        elif key == keyboard.KEY_ENTER:
            return self.selected_item()
        elif key == curses.KEY_MOUSE:
            x, y = self.getxy()
            mouse_event = curses.getmouse()
            if self.lambda_x(x) <= mouse_event[1] and self.lambda_x(x) + self.lambda_w(x) >= mouse_event[1]:  # type: ignore[misc]
                if self.lambda_y(y) <= mouse_event[2] and self.lambda_y(y) + self.lambda_h(y) >= mouse_event[2]:  # type: ignore[misc]
                    return self.handle_mouse_input(mouse_event, x, y)
        return None

    def selected_item(self) -> Optional[str]:
        return self.buffer[self.cursor]

    def handle_mouse_input(self, mouse_event: Tuple[int, int, int, int, Any], _: int, y: int) -> Optional[str]:
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            try:
                return self.buffer[self.pad_pos_y + mouse_event[2] - self.lambda_y(y) - 1]
            except IndexError:
                pass
        return None

    def add_new(self, name: str) -> None:
        """
        Add a new item in the listview without updating the it.

        Args:
            name: The new item
        """
        self.buffer.append(name)

    def set_buffer(self, buff: List[str]) -> None:
        """
        Display the provided list of items.

        Args:
            buff: The new buffer which is going to be displayed
        """
        self.buffer = buff
        self.cursor_border = len(self.buffer) - 1
        self.draw()
