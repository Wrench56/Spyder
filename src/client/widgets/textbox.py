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

        self.buffer = ['']

        self.pad_pos_x = 0
        self.pad_pos_y = 0

        self.cur_x = 0
        self.cur_y = 0
        self.width = width
        self.height = height

        self.show_chars = show_chars

        self.pad = curses.newpad(self.height, self.width)
        self.pad.scrollok(True)

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super().getxy()
        ly = self.lambda_y(y)
        lx = self.lambda_x(x)
        self.move_cursor(lx, ly)

        self.empty()
        for i, line in enumerate(self.buffer):
            if self.show_chars:
                line = self.show_chars * len(line)  # type: ignore[assignment]
            self.pad.addstr(i, 0, line)

        sy, sx = self.stdscr.getbegyx()
        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, sy+ly, sx+lx, sy+ly+self.lambda_h(y), sx+lx+self.lambda_w(x))  # type: ignore[misc] # noqa: E226

    def input(self, ch: int) -> None:
        """
        Interpreters given keystrokes.

        Args:
            ch: The pressed key's value
        """
        x, y = super().getxy()

        if ch == keyboard.KEY_BACKSPACE:
            if self.cur_x > 0:
                self.buffer[self.cur_y] = self.buffer[self.cur_y][:self.cur_x - 1] + self.buffer[self.cur_y][(self.cur_x):]
                self.cur_x -= 1
        elif ch == keyboard.KEY_DELETE:
            if self.cur_x < self.lambda_w(x):  # type: ignore[misc]
                self.buffer[self.cur_y] = self.buffer[self.cur_y][:self.cur_x] + self.buffer[self.cur_y][(self.cur_x + 1):]
        elif ch == keyboard.KEY_ENTER:
            if self.pad_pos_y + 1 < self.height:
                self.cur_y += 1
                self.cur_x = 0
                self.buffer.append('')
        elif ch == curses.KEY_DOWN:
            if self.pad_pos_y < self.pad.getyx()[0] - 1:
                self.cur_y += 1
                if self.cur_y > self.height:
                    self.pad_pos_y += 1
        elif ch == curses.KEY_UP:
            if self.pad_pos_y > 0:
                self.cur_y -= 1
                self.pad_pos_y -= 1
        elif ch == curses.KEY_LEFT:
            if self.cur_x > 0:
                self.cur_x -= 1
        elif ch == curses.KEY_RIGHT:
            if self.cur_x < self.lambda_w(x):  # type: ignore[misc]
                self.cur_x += 1
        else:
            if self.cur_x < self.lambda_w(x):  # type: ignore[misc]
                self.cur_x += 1
                self.buffer[self.cur_y] += chr(ch)

        self.draw()

        lx, ly = self.lambda_x(x), self.lambda_y(y)
        self.move_cursor(lx, ly)

    def move_cursor(self, lx: int, ly: int) -> None:
        sy, sx = self.stdscr.getbegyx()
        cursor.move(sx + lx + self.cur_x, sy + ly + self.cur_y)

    def update_cursor(self) -> None:
        """Update the cursor's position."""
        x, y = super().getxy()
        lx, ly = self.lambda_x(x), self.lambda_y(y)

        self.move_cursor(lx, ly)

    def empty(self) -> None:
        """Empty the text buffer."""
        for y, line in enumerate(self.buffer):
            self.pad.addstr(y, 0, ' ' * (len(line) + 1))  # +1 because of the backspace operation...

    def get_text(self) -> str:
        """
        Return the text buffer.

        Returns:
            str: The text buffer
        """
        return '\n'.join(self.buffer)
