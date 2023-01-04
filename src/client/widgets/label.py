import curses

from widgets import widget
from utils import colors


class Label(widget.Widget):
    def __init__(self, stdscr: curses.window, text: str):
        self.text = text
        super().__init__(stdscr)

    def draw(self):
        x, y = super().getxy()
        colors.colored_addstr(self.stdscr, self.lambda_x(x), self.lambda_y(y), self.text)

        self.stdscr.refresh()

    def set_text(self, text):
        self.text = text
        self.draw()


class MultilineLabel(Label):
    def __init__(self, stdscr: curses.window, text: str):
        super().__init__(stdscr, text)

    def draw(self):
        x, y = super().getxy()
        for i, line in enumerate(self.text.split('\n')):
            colors.colored_addstr(self.stdscr, self.lambda_x(x), self.lambda_y(y) + i, str(line))

        self.stdscr.refresh()
