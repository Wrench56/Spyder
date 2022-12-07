import curses

from widgets import widget
from utils import colors
class Label(widget.Widget):
    def __init__(self, stdscr, text, color=None):
        self.text = text

        if color == None:
            self.color = curses.color_pair(colors.WHITE_ON_BLACK)
        else:
            self.color = color
        
        super().__init__(stdscr)

    def draw(self):
        x, y = super().getxy()

        self.stdscr.addstr(self.lambda_y(y), self.lambda_x(x), self.text, self.color)
        self.stdscr.refresh()

    def set_text(self, text):
        self.text = text
        self.draw()


class MultilineLabel(Label):
    def __init__(self, stdscr, text, color=None):
        super().__init__(stdscr, text, color=color)

    def draw(self):
        x, y = super().getxy()
        for i, line in enumerate(self.text.split('\n')):
            self.stdscr.addstr(self.lambda_y(y)+i, self.lambda_x(x), f'{line}\n', self.color)
            
        self.stdscr.refresh()