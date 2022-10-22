from widgets import widget, label
from utils import keyboard
import curses

class Textbox(widget.Widget):
    def __init__(self, stdscr, width = 20, height = 100, show_chars = False):
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

    def draw(self):
        x, y = super().getxy()

        self.empty()
        for i, line in enumerate(self.buffer):
            if self.show_chars:
                line = len(line)*self.show_chars
            self.pad.addstr(i, 0, line)

        sy, sx = self.stdscr.getbegyx()
        ly = self.lambda_y(y)
        lx = self.lambda_x(x)
        self.move_cursor(lx, ly)
        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, sy+ly, sx+lx, sy+ly+self.lambda_h(y), sx+lx+self.lambda_w(x))

    def input(self, ch):
        x, y = super().getxy()

        if ch == keyboard.KEY_BACKSPACE:
            if self.cur_x > 0:
                self.buffer[self.cur_y] = self.buffer[self.cur_y][:self.cur_x-1] + self.buffer[self.cur_y][(self.cur_x):]
                self.cur_x -= 1
        elif ch == keyboard.KEY_DELETE:
            if self.cur_x < self.lambda_w(x):
                self.buffer[self.cur_y] = self.buffer[self.cur_y][:self.cur_x] + self.buffer[self.cur_y][(self.cur_x+1):]
        elif ch == keyboard.KEY_ENTER:
            if self.pad_pos_y+1 < self.height:
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
            if self.cur_x < self.lambda_w(x):
                self.cur_x += 1
        else:
            if self.cur_x < self.lambda_w(x):
                self.cur_x += 1
                self.buffer[self.cur_y] += chr(ch)
            
        self.draw()

        lx, ly = self.lambda_x(x), self.lambda_y(y)
        self.move_cursor(lx, ly)

    def move_cursor(self, lx, ly):
        self.stdscr.cursyncup()
        self.stdscr.move(ly+self.cur_y, lx+self.cur_x)

    def update_cursor(self): #? Most likely not needed
        x, y = super().getxy()
        lx, ly = self.lambda_x(x), self.lambda_y(y)

        self.move_cursor(lx, ly)



    def empty(self):
        for y, line in enumerate(self.buffer):
            self.pad.addstr(y, 0, ' '*(len(line)+1)) # +1 because of the backspace operation...
