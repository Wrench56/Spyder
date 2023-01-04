from widgets import widget
from utils import keyboard, colors

import curses


class ListView(widget.Widget):
    def __init__(self, stdscr: curses.window, width: int = 20, height: int = 100):
        super().__init__(stdscr)

        self.buffer = []

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
        self.draw_items()

        sy, sx = self.stdscr.getbegyx()
        self.pad.refresh(self.pad_pos_y, self.pad_pos_x, sy+ly, sx+lx, sy+ly+self.lambda_h(y), sx+lx+self.lambda_w(x))  # noqa: E226

    def draw_items(self):
        for i, item in enumerate(self.buffer):
            colors.colored_addstr(self.pad, 0, i, item)

    def input(self, key: int) -> None | str:
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
            return self.selected_item()
        elif key == curses.KEY_MOUSE:
            x, y = self.getxy()
            mouse_event = curses.getmouse()
            if self.lambda_x(x) <= mouse_event[1] and self.lambda_x(x) + self.lambda_w(x) >= mouse_event[1]:
                if self.lambda_y(y) <= mouse_event[2] and self.lambda_y(y) + self.lambda_h(y) >= mouse_event[2]:
                    return self.handle_mouse_input(mouse_event, x, y)

    def selected_item(self):
        return self.buffer[self.cursor]

    def handle_mouse_input(self, mouse_event: tuple, x: int, y: int):
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            try:
                return self.buffer[self.pad_pos_y + mouse_event[2] - self.lambda_y(y) - 1]
            except IndexError:
                pass

    def add_new(self, name: str):
        self.buffer.append(name)

    def set_buffer(self, buff: list):
        self.buffer = buff
        self.draw()
