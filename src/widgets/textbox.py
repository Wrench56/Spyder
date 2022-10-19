from widgets import widget, label
from utils import keyboard
import curses

class Textbox(widget.Widget):
    def __init__(self, stdscr, width = 20, height = 100):
        super().__init__(stdscr)

        self.label = label.Label(self.stdscr,'@')
        self.label.set_size(lambda x: 10, lambda y: 10)
        self.label.draw(0, 0)

        self.buffer = ['']

        self.pad_pos_x = 0
        self.pad_pos_y = 0

        self.cur_x = 0
        self.cur_y = 0
        self.width = width
        self.height = height


        self.pad = curses.newpad(self.height, self.width)
        self.pad.scrollok(True)

    def draw(self, x, y):
        self.last_x = x
        self.last_y = y

        self.empty()
        for i, line in enumerate(self.buffer):
            self.pad.addstr(i, 0, line)

        ly = self.lambda_y(y)
        lx = self.lambda_x(x)
        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, ly, lx, ly+self.height, lx+self.width)
        self.stdscr.refresh()

    def input(self, ch):
        if ch == keyboard.KEY_BACKSPACE:
            if self.cur_x > 0:
                self.buffer[self.cur_y] = self.buffer[self.cur_y][:self.cur_x-1] + self.buffer[self.cur_y][(self.cur_x+1):]
                self.cur_x -= 1
                self.pad.addstr(self.cur_y, self.cur_x, ' ')
        elif ch == keyboard.KEY_ENTER:
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
        else:
            self.cur_x += 1
            self.buffer[self.cur_y] += chr(ch)
            
            
        self.label.set_text(str(self.cur_x))
        self.draw(self.last_x, self.last_y)
        self.stdscr.move(self.cur_y, self.cur_x)
        self.stdscr.refresh()

    def set_size(self, lambda_x, lambda_y):
        super().set_size(lambda_x, lambda_y)

    def empty(self):
        for y, line in enumerate(self.buffer):
            self.stdscr.addstr(self.lambda_y(self.last_x)+y, self.lambda_x(self.last_x), ' '*len(line))