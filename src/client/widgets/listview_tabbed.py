from typing import List, Dict, Callable, Optional

import curses

from widgets.label import Label
from widgets.listview_e import ListViewE
from widgets.listview_node import Node
from widgets.widget import Widget

from utils import keyboard, colors


class ListViewTabbed(Widget):
    def __init__(self, stdscr: object, width: int = 20, height: int = 100) -> None:
        super().__init__(stdscr)

        self.tabs: Dict[str, List[Node]] = {'Default': [Node('Hello', [Node('A', [Node('1'), Node('2')], False), Node('B', [Node('1'), Node('2')]), Node('C', [Node('1'), Node('2')], True)])], 'Chats': [Node('Hello', [Node('A', [Node('1'), Node('2')], False), Node('B', [Node('1'), Node('2')])])], 'SAAAAAAAAAAAAAAAE': [Node('E')], 'SBBBBBBBBBBBBBBBBBBBBBE': [Node('F')], 'SCCCCCCCCCCCCCCCCCCCCCCE': [Node('G')]}

        self.pad_cursor_x = 0
        self.start_item = 0
        self.cursor = 0

        self.listview = ListViewE(self.stdscr, width, height)

        self.sep_label = Label(self.stdscr, '')

        self.tab_pad = curses.newpad(1, 1000)
        self.tab_pad.scrollok(True)

    def set_size(self, lambda_x: Callable[[int], int], lambda_y: Callable[[int], int], lambda_w: Optional[Callable[[int], int]], lambda_h: Optional[Callable[[int], int]]) -> None:
        super().set_size(lambda_x, lambda_y, lambda_w, lambda_h)

        self.listview.set_size(self.lambda_x, lambda y: self.lambda_y(y) + 2, self.lambda_w, lambda h: self.lambda_h(h) - 2)  # type: ignore[misc]
        self.sep_label.set_size(lambda x: self.lambda_x(x) - 1, lambda _: 2, None, None)

    def draw(self) -> None:
        x, y = super().getxy()
        ly = self.lambda_y(y)
        lx = self.lambda_x(x)

        sy, sx = self.stdscr.getbegyx()
        colors.colored_addstr(self.stdscr, lx, ly, '<')
        colors.colored_addstr(self.stdscr, self.lambda_w(x) + lx, ly, '>')  # type: ignore[misc]

        for x_plc in (lx + 1, self.lambda_w(x)):  # type: ignore[misc]
            colors.colored_addstr(self.stdscr, x_plc, ly - 1, '┬')
            colors.colored_addstr(self.stdscr, x_plc, ly, '│')

        colors.colored_addstr(self.stdscr, lx - 1, ly + 1, f'├─┴{"─" * (self.lambda_w(x) - 3)}┴─┤')  # type: ignore[misc]
        self.stdscr.refresh()

        x_pos = 0
        for i, tab in enumerate(self.tabs.keys()):
            color = ''
            reset = ''
            sep = ''
            if i == self.cursor:
                color = '\x1b[47m\x1b[30m'
                reset = '\x1b[0m'
            if i < len(self.tabs.keys()) - 1:
                sep = '|'
            colors.colored_addstr(self.tab_pad, x_pos, 0, f'{color} {tab} {reset}{sep}')
            x_pos += len(tab) + 3

        self.listview.resize(x, y)

        self.calculate_pad_scroll()
        self.tab_pad.refresh(0, self.pad_cursor_x, sy+ly, sx+lx+2, sy+ly, sx+lx+self.lambda_w(x)-4)  # type: ignore[misc] # noqa: E226
        self.listview.set_buffer(self.tabs[list(self.tabs.keys())[self.cursor]])

    # def horizontal_scroll(self, x: int) -> None:
    #    items_till_cursor = tuple(self.tabs.keys())[self.start_item:self.cursor + 1]
    #    if sum(map(len, items_till_cursor)) + len(items_till_cursor) * 3 >= self.lambda_w(x):
    #        self.pad_cursor_x += len(items_till_cursor[0]) + 3
    #        self.start_item += 1
    #        self.horizontal_scroll(x)

    def calculate_pad_scroll(self) -> None:
        items_till_cursor = tuple(self.tabs.keys())[:self.cursor]
        self.pad_cursor_x = sum(map(len, items_till_cursor)) + len(items_till_cursor) * 3

    def input(self, key: int) -> Optional[str]:
        if key == keyboard.KEY_TAB:
            # Next tab
            if self.cursor < len(self.tabs.keys()) - 1:
                self.cursor += 1
            else:
                self.cursor = 0
        elif key == keyboard.KEY_SHIFT_TAB:
            # Previous tab
            if self.cursor > 0:
                self.cursor -= 1
            else:
                self.cursor = len(self.tabs.keys()) - 1
        elif key == curses.KEY_MOUSE:
            x, y = self.getxy()
            sy, sx = self.stdscr.getbegyx()
            mouse_event = curses.getmouse()
            if self.lambda_y(y) + sy == mouse_event[2]:
                # Previous tab
                if sx + 1 == mouse_event[1]:
                    if self.cursor > 0:
                        self.cursor -= 1
                        self.calculate_pad_scroll()
                        self.listview.cursor = 0
                        self.draw()
                # Next tab
                elif self.lambda_w(x) + sx + 1 == mouse_event[1]:  # type: ignore[misc]
                    if self.cursor < len(self.tabs.keys()) - 1:
                        self.cursor += 1
                        self.calculate_pad_scroll()
                        self.listview.cursor = 0
                        self.draw()
                # Select tab with mouse
                elif sx + 1 < mouse_event[1] < self.lambda_w(x) + sx + 1:  # type: ignore[misc]
                    pass

            return self.listview.input(key)
        else:
            return self.listview.input(key)

        # Reset the cursor of the listview
        self.listview.cursor = 0
        self.draw()
        return None
