from typing import List, Tuple, Any, Optional

import curses

from widgets.listview import ListView
from widgets.listview_node import Node


class ListViewE(ListView):
    def __init__(self, stdscr: object, width: int = 20, height: int = 100):
        super().__init__(stdscr, width, height)
        self.buffer: List[Node] = []  # type: ignore[assignment]
        self.flattend_buffer: List[Node] = [] # type: ignore[assignment]

    def draw_items(self) -> None:
        line = 0
        for item in self.buffer:
            line = item.draw(self.pad, line)

    def handle_mouse_input(self, mouse_event: Tuple[int, int, int, int, Any], _: int, y: int) -> Optional[str]:
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            try:
                node = self.flattend_buffer[self.pad_pos_y + mouse_event[2] - self.lambda_y(y) - 1]
                if len(node.nodes) == 0:
                    return node
                else:
                    node.toggle_state()
                    self.draw()
            except IndexError:
                # User didn't click on menu point
                pass
        return None
    
    def selected_item(self) -> Optional[str]:
        node = self.flattend_buffer[self.cursor]
        if len(node.nodes) == 0:
            return node.full_path
        else:
            node.toggle_state()
            self.draw()

    def get_item(self, path: str) -> Optional[object]:
        path_segments = path.split('/')
        for item in self.buffer:
            if item.name == path_segments[0]:
                return item.get_node(path_segments[1:])
        return None

    def add_new_node(self, path: str, node: Node) -> None:
        self.get_item(path).add_node(node)
        node.set_full_path(path)

    def create_flattend_buffer(self):
        self.flattend_buffer = []
        for node in self.buffer:
            self.flattend_buffer.extend(node.flatten())
        
        self.cursor_border = len(self.flattend_buffer) - 1

    def set_buffer(self, buff: List[Node], refresh=False) -> None:  # type: ignore[override]
        self.buffer = buff
        # This might be slow!
        for node in self.buffer:
            node.set_full_path('', refresh=refresh)
        self.create_flattend_buffer()
        self.draw()
