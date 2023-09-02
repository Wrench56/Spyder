"""This module implements a textbox widget with curses."""
import curses

from widgets import widget
from utils import keyboard, cursor


class Textbox(widget.Widget):
    """A multi-line textbox widget with scroll capabilities."""

    def __init__(self, stdscr: object, width: int = 20, height: int = 100, show_chars: bool | str = False):
        """
        Create the textbox widget without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            width: The width of the pad
            height: The height of the pad representing the maximum
                    lines that can be written in the textbox
            show_chars: Whether to show special characters instead
                        the ones typed in. This can be useful for
                        password inputs. By default it is False.
                        Specify a string (character) to display that
                        instead of the actual input.
        """
        super().__init__(stdscr)

        self._buffer = ['']

        self._pad_pos_x = 0
        self._pad_pos_y = 0

        self._cur_x = 0
        self._cur_y = 0
        self._width = width
        self._height = height

        self._show_chars = show_chars

        self._pad = curses.newpad(self._height, self._width)
        self._pad.scrollok(True)

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super()._getxy()
        ly = self._lambda_y(y)
        lx = self._lambda_x(x)
        self._move_cursor(lx, ly)

        self.empty()
        for i, line in enumerate(self._buffer):
            if self._show_chars:
                line = self._show_chars * len(line)  # type: ignore[assignment]
            self._pad.addstr(i, 0, line)

        sy, sx = self._stdscr.getbegyx()
        self._pad.refresh(self._pad_pos_y, self._pad_pos_x, sy+ly, sx+lx, sy+ly+self._lambda_h(y), sx+lx+self._lambda_w(x))  # type: ignore[misc] # noqa: E226

    def input(self, ch: int) -> None:
        """
        Interpreters given keystrokes.

        Args:
            ch: The pressed key's value
        """
        x, y = super()._getxy()

        if ch == keyboard.KEY_BACKSPACE:
            if self._cur_x > 0:
                self._buffer[self._cur_y] = self._buffer[self._cur_y][:self._cur_x - 1] + self._buffer[self._cur_y][(self._cur_x):]
                self._cur_x -= 1
        elif ch == keyboard.KEY_DELETE:
            if self._cur_x < self._lambda_w(x):  # type: ignore[misc]
                self._buffer[self._cur_y] = self._buffer[self._cur_y][:self._cur_x] + self._buffer[self._cur_y][(self._cur_x + 1):]
        elif ch == keyboard.KEY_ENTER:
            if self._pad_pos_y + 1 < self._height:
                self._cur_y += 1
                self._cur_x = 0
                self._buffer.append('')
        elif ch == curses.KEY_DOWN:
            if self._pad_pos_y < self._pad.getyx()[0] - 1:
                self._cur_y += 1
                if self._cur_y > self._height:
                    self._pad_pos_y += 1
        elif ch == curses.KEY_UP:
            if self._pad_pos_y > 0:
                self._cur_y -= 1
                self._pad_pos_y -= 1
        elif ch == curses.KEY_LEFT:
            if self._cur_x > 0:
                self._cur_x -= 1
        elif ch == curses.KEY_RIGHT:
            if self._cur_x < self._lambda_w(x):  # type: ignore[misc]
                self._cur_x += 1
        else:
            if self._cur_x < self._lambda_w(x):  # type: ignore[misc]
                self._cur_x += 1
                self._buffer[self._cur_y] += chr(ch)

        self.draw()

        lx, ly = self._lambda_x(x), self._lambda_y(y)
        self._move_cursor(lx, ly)

    def _move_cursor(self, lx: int, ly: int) -> None:
        sy, sx = self._stdscr.getbegyx()
        cursor.move(sx + lx + self._cur_x, sy + ly + self._cur_y)

    def update_cursor(self) -> None:
        """Update the cursor's position."""
        x, y = super()._getxy()
        lx, ly = self._lambda_x(x), self._lambda_y(y)

        self._move_cursor(lx, ly)

    def empty(self) -> None:
        """Empty the text buffer."""
        for y, line in enumerate(self._buffer):
            self._pad.addstr(y, 0, ' ' * (len(line) + 1))  # +1 because of the backspace operation...

    @property
    def text(self) -> str:
        """
        Convert and return the text buffer.

        Returns:
            str: The text in string
        """
        return '\n'.join(self._buffer)

    @text.setter
    def text(self, text: str) -> None:
        self._buffer = text.split('\n')
        self.update_cursor()
