"""This module implements a multi-line label widget with curses."""

from utils import colors
from widgets.label import Label


class MultilineLabel(Label):
    """A label widget capable of displaying multiple lines of text."""

    def draw(self) -> None:
        """Draw the widget."""
        x, y = super().getxy()
        for i, line in enumerate(self.text.split('\n')):
            colors.colored_addstr(self.stdscr, self.lambda_x(x), self.lambda_y(y) + i, str(line))

        self.stdscr.refresh()
