"""This module implements the enhanced listview widget with curses."""

from typing import List, Tuple, Any, Optional

import curses

from widgets.listview import ListView
from widgets.listview_node import ListViewNode


class ListViewE(ListView):
    """
    The enhanced listview widget capable of displaying Node()-s.

    This widget - compared to the regular listview widget - is capable
    of displaying expandable and collapsable Node()-s. Node()-s can
    represent trees (e.g.: A file tree).
    """

    def __init__(self, stdscr: object, width: int = 20, height: int = 100):
        """
        Create the enhanced listview without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            width: The width of the pad
            height: The height of the pad representing the maximum
                    elements that can be added to the listview
        """
        super().__init__(stdscr, width, height)
        self._buffer: List[ListViewNode] = []  # type: ignore[assignment]
        self._flattend_buffer: List[ListViewNode] = []

    def _draw_items(self) -> None:
        line = 0
        for item in self._buffer:
            line = item.draw(self._pad, line)

    def _handle_mouse_input(self, mouse_event: Tuple[int, int, int, int, Any], _: int, y: int) -> Optional[str]:
        if mouse_event[4] == curses.BUTTON1_CLICKED:
            try:
                node = self._flattend_buffer[self._pad_pos_y + mouse_event[2] - self._lambda_y(y) - 1]
                if len(node.nodes) == 0:
                    return node.full_path
                node.toggle_state()
                self.draw()
            except IndexError:
                # User didn't click on menu point
                pass
        return None

    def _selected_item(self) -> Optional[str]:
        node = self._flattend_buffer[self._cursor]
        if len(node.nodes) == 0:
            return node.full_path
        node.toggle_state()
        self._create_flattend_buffer()
        self.draw()

        return None

    def get_item(self, path: str) -> Optional[object]:
        """
        Return a ListViewNode() by specifying its absolute path.

        Args:
            path: A string representing the path to the target
                  ListViewNode(). The path should include all parent
                  nodes by their name separated by a "/" character.
                  After the last parent node, the target node's name
                  should be specified.
                  For example: 'parent1/parent2/target'

        Returns:
            Optional[object]: Returns the target Node() or None if the
                              target node was not found
        """
        path_segments = path.split('/')
        for item in self._buffer:
            if item.name == path_segments[0]:
                return item.get_node(path_segments[1:])
        return None

    def add_new_node(self, path: str, node: ListViewNode) -> None:
        """
        Add a new Node() with specified path.

        Args:
            path: The path targeting the parent node to which the
                  specified node is going to be appended. The path
                  is structured the same way as get_item().
                  For example: 'parent1/parent2'
            node: A ListViewNode() object that is going to be
                  appended to the parent node specified by the path
        """
        self.get_item(path).add_node(node)
        node.set_full_path(path)

    def _create_flattend_buffer(self) -> None:
        self._flattend_buffer = []
        for node in self._buffer:
            self._flattend_buffer.extend(node.flatten())

        self._cursor_border = len(self._flattend_buffer) - 1

    def set_buffer(self, buff: List[ListViewNode], refresh: bool = False) -> None:  # type: ignore[override]
        """
        Display the provided list of items.

        Args:
            buff: The new buffer which is going to be displayed
            refresh: If true, refresh the absolute path for
            all nodes. False by default
        """
        self._buffer = buff
        # This might be slow!
        for node in self._buffer:
            node.set_full_path('', refresh=refresh)
        self._create_flattend_buffer()
        self.draw()
