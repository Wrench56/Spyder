from widgets import widget, label
from utils import keyboard, colors

import curses

class ListView(widget.Widget):
    def __init__(self, stdscr, width=20, height=100):
        super().__init__(stdscr)

        self.buffer = ['']

        self.pad_pos_x = 0
        self.pad_pos_y = 0

        self.pad = curses.newpad(height, width)
        self.pad.scrollok(True)

    def draw(self):
        x, y = super().getxy()
        ly = self.lambda_y(y)
        lx = self.lambda_x(x)

        self.empty()
        for i, line in enumerate(self.buffer):
            colors.colored_addstr(self.pad, 0, i, line)

        sy, sx = self.stdscr.getbegyx()
        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, sy+ly, sx+lx, sy+ly+self.lambda_h(y), sx+lx+self.lambda_w(x))

    def empty(self):
        for y, line in enumerate(self.buffer):
            self.pad.addstr(y, 0, ' '*(len(line))) # +1 because of the backspace operation...

    def add_text(self, text):
        self.buffer.append(text)
        self.draw()

    def get_text(self):
        return '\n'.join(self.buffer)