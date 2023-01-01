from widgets.listview import ListView
from widgets.listview_node import Node

import curses


class ListViewE(ListView):
    def __init__(self, stdscr, width=20, height=100):
        super().__init__(stdscr, width, height)
        self.buffer = []

    def draw_items(self):
        line = 0
        for item in self.buffer:
            line = item.draw(self.pad, line)

    def handle_mouse_input(self, mouse_event, x, y):
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            result = 0
            for node in self.buffer:
                result = node.get_by_index(self.pad_pos_y+mouse_event[2]-self.lambda_y(y), result)
                if isinstance(result, str):
                    return result
                if isinstance(result, bool):
                    break
            self.draw()

    def get_item(self, path: str):
        path_segments = path.split('/')
        for item in self.buffer:
            if item.name == path_segments[0]:
                return item.get(path_segments[1:])

    def add_new(self, path: str, node: Node):
        self.get_item(path).add_node(node)
