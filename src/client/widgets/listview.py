from widgets import widget, label, subwindow, listview_utils
from utils import keyboard, colors

import curses

class ListView(widget.Widget):
    def __init__(self, stdscr, width=20, height=100, border=False):
        super().__init__(stdscr)

        self.buffer = ['Hello', [True, 'Friend', 'World', [False, 'Universe', 'Multiverse']], 'Mark', [True, 'Wrd', [True, 'A', 'B'], 'CRD']]

        self.pad_pos_x = 0
        self.pad_pos_y = 0

        self.cursor = 0

        self.width = width
        self.height = height

        self.pad = curses.newpad(height, width)
        self.pad.scrollok(True)
        

    def draw(self):
        x, y = super().getxy()
        ly = self.lambda_y(y)
        lx = self.lambda_x(x)

        self.pad.erase()
        listview_utils.draw_tree(self.pad, self.buffer, 0, '')

        sy, sx = self.stdscr.getbegyx()
        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, sy+ly, sx+lx, sy+ly+self.lambda_h(y), sx+lx+self.lambda_w(x))

    def input(self, key) -> None|str:
        if key == curses.KEY_DOWN:
            if self.cursor >= self.height:
                return
            self.cursor += 1
            self.draw()
        elif key == curses.KEY_UP:
            if self.cursor == 0:
                return
            self.cursor -= 1
            self.draw()
        elif key == keyboard.KEY_ENTER:
            if not listview_utils.toggle_expand(self.buffer, self.cursor):
                return listview_utils.flatten(self.buffer)[self.cursor]
            else:
               self.draw()
        elif key == curses.KEY_MOUSE:
            return self.handle_mouse_input()

    def handle_mouse_input(self):
        x, y = self.getxy()
        mouse_event = curses.getmouse()
        if self.lambda_x(x) <= mouse_event[1] and self.lambda_x(x)+self.lambda_w(x) >= mouse_event[1]:
            if self.lambda_y(y) <= mouse_event[2] and self.lambda_y(y)+self.lambda_h(y) >= mouse_event[2]:
                if mouse_event[4] == curses.BUTTON1_CLICKED:
                    try:
                        clicked_node = listview_utils.flatten(self.buffer)[self.pad_pos_y+mouse_event[2]-self.lambda_x(x)-1]
                        if not listview_utils.toggle_expand(self.buffer, self.pad_pos_y+mouse_event[2]-self.lambda_x(x)-1):
                            return clicked_node
                        else:
                            self.draw()
                    except IndexError:
                        pass

    def set_buffer(self, buff):
        self.buffer = buff
        self.draw()

    def get_text(self):
        return '\n'.join(self.buffer)