"""This module implements a label widget with curses."""

from widgets import widget
from utils import colors


class Label(widget.Widget):
    """A label widget capable of displaying a one-line text."""

    def __init__(self, stdscr: object, text: str) -> None:
        """
        Create the label without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            text: The string displayed on the widget
        """
        self.text = text
        super().__init__(stdscr)

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super().getxy()
        colors.colored_addstr(self.stdscr, self.lambda_x(x), self.lambda_y(y), self.text)

        self.stdscr.refresh()

    def set_text(self, text: str) -> None:
        """
        Set the text displayed on the widget.

        Args:
            text: The string displayed on the widget
        """
        self.text = text
        self.draw()
