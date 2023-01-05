from typing import List, Tuple, Any, Optional

import curses

from widgets.listview import ListView
from widgets.listview_node import Node


class ListViewE(ListView):
    def __init__(self, stdscr: object, width: int = 20, height: int = 100):
        super().__init__(stdscr, width, height)
        self.buffer: List[Node] = []  # type: ignore[assignment]

    def draw_items(self) -> None:
        line = 0
        for item in self.buffer:
            line = item.draw(self.pad, line)

    def handle_mouse_input(self, mouse_event: Tuple[int, int, int, int, Any], _: int, y: int) -> Optional[str]:
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            result = 0
            for node in self.buffer:
                result = node.get_by_index(self.pad_pos_y + mouse_event[2] - self.lambda_y(y), result)  # type: ignore[assignment]
                if isinstance(result, str):
                    return result
                if isinstance(result, bool):
                    break
            self.draw()
        return None

    def get_item(self, path: str) -> Optional[object]:
        path_segments = path.split('/')
        for item in self.buffer:
            if item.name == path_segments[0]:
                return item.get_node(path_segments[1:])
        return None

    def add_new_node(self, path: str, node: Node) -> None:
        self.get_item(path).add_node(node)
