from widgets import widget
import math

class Label(widget.Widget):
    def __init__(self, stdscr, text):
        self.text = text
        super().__init__(stdscr)

    def draw(self, x, y):
        self.last_x = x
        self.last_y = y

        self.stdscr.addstr(self.lambda_y(y), self.lambda_x(x)-self.calculate_text_size(self.text), self.text)
        self.stdscr.refresh()

    def calculate_text_size(self, text):
        return math.floor(len(text) / 2)

    def set_text(self, text):
        self.text = text
        self.draw(self.last_x, self.last_y)