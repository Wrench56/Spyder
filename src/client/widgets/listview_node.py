"""
This module implements the ListViewNode().

The node is used by the enhanced and tabbed listview widgets.
"""

from typing import List, Optional, Union, Literal

from utils.colors import colored_addstr


class ListViewNode:
    """
    A listview node which can contain several other nodes.

    These nodes can be useful to represent trees (e.g.: file trees).
    The nodes can be expanded or collapsed.
    """

    def __init__(self, name: str, nodes: Optional[List['ListViewNode']] = None, is_expanded: bool = True) -> None:
        """
        Create a node.

        Args:
            name: The displayed name of the node
            nodes: A list of all child nodes of this node. By default
                   it is None implying that this is only a child node.
            is_expanded: Whether to set the node's initial state
                         expanded or collapsed. Default value is True
        """
        self.name: str = name
        self.full_path: str = ''

        if nodes is None:
            nodes = []
        self.nodes: List['ListViewNode'] = nodes
        self.is_expanded: bool = is_expanded

    def set_full_path(self, path: str, refresh: bool = True) -> None:
        """
        Set the absolute path for all child node and for itself.

        Args:
            path: The absolute path leading to this node.
            refresh: Whether to refresh the already set full_path
                     variable with the new provided path or only
                     set the full_path variable if it was previously
                     not set
        """
        if not refresh and self.full_path != '':
            return
        if self.full_path == f'{path}{self.name}':
            return

        self.full_path = f'{path}{self.name}'
        for node in self.nodes:
            node.set_full_path(f'{self.full_path}/')

    def toggle_state(self) -> bool:
        """
        Simply toggle the collapsed/expanded state.

        Returns:
            bool: True if operation was successful, otherwise False.
                  If this node is a child node without other child
                  nodes, False is returned
        """
        if len(self.nodes) > 0:
            self.is_expanded = not self.is_expanded
            return True
        return False

    def add_node(self, node_obj: 'ListViewNode') -> None:
        """
        Add a child node.

        Args:
            node_obj: The ListViewNode() object which is going to be
                      added to the child nodes
        """
        self.nodes.append(node_obj)
        node_obj.set_full_path(self.full_path)

    def get_node(self, path: List[str]) -> Union[Literal[False], 'ListViewNode']:
        """
        Return a child node by specifying its absolute path.

        Args:
            path: An ordered list of the parent nodes (each parent
                  node name being one element) and the target node's
                  name at the end of the list.
                  For example: ['parent1', 'parent2', 'target']

        Returns:
            Union[False, ListViewNode]: Returns the targeted node if
                                        it exists in one of the child
                                        nodes or their child nodes.
                                        Returns False if it could not
                                        be found
        """
        for node in self.nodes:
            if node.name == path[0]:
                return node.get_node(path[1:])
        return False

    # Older versions of Python do not support forward referencing
    def flatten(self) -> List['ListViewNode']:
        """
        Create a 1 dimensional list with the node and child nodes.

        Returns:
            List[ListViewNode]: A list of the node itself and all of
                                its child nodes
        """
        flattend_list: List['ListViewNode'] = [self]
        if self.is_expanded:
            for node in self.nodes:
                flattend_list.extend(node.flatten())

        return flattend_list

    def draw(self, pad: object, line: int, tab: str = '') -> int:
        """
        Draw the node and all of its child nodes.

        Args:
            pad: The curses pad object on which the nodes will be drawn
            line: The y coordinate (= n-th line) on which the node will
                  be drawn
            tab: The indentation of the node. The child nodes have a
                 different indentation compared to their parents
                 For example:
                    - parent
                        - child_a
                        - child_b

        Returns:
            int: The last line used by this node to draw itself and its
                 underlying child nodes
        """
        if len(self.nodes) > 0:
            if self.is_expanded:
                ec_char = '▾'
            else:
                ec_char = '▸'
        else:
            ec_char = '╴'
        colored_addstr(pad, 2, line, f'{tab}{ec_char}{self.name}')
        line += 1
        if not self.is_expanded:
            return line
        for i, node in enumerate(self.nodes):
            if len(self.nodes) - 1 == i:
                new_tab = '└'
            else:
                new_tab = '├'
            line = node.draw(pad, line, tab=tab.replace('├', '│').replace('└', ' ') + new_tab)

        return line
