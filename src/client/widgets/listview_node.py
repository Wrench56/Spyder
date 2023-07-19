from typing import List, Optional, Union, Literal

from utils.colors import colored_addstr


class Node:
    def __init__(self, name: str, nodes: Optional[List['Node']] = None, is_expanded: bool = True) -> None:
        self.name: str = name
        self.full_path: str = ''

        if nodes is None:
            nodes = []
        self.nodes: List['Node'] = nodes
        self.is_expanded: bool = is_expanded

    def set_full_path(self, path: str, refresh: bool = True):
        if not refresh and self.full_path != '':
            return
        if self.full_path == f'{path}{self.name}':
            return

        self.full_path = f'{path}{self.name}'
        for node in self.nodes:
            node.set_full_path(f'{self.full_path}/')

    def toggle_state(self) -> bool:
        if len(self.nodes) > 0:
            self.is_expanded = not self.is_expanded
            return True
        return False

    def add_node(self, node_obj: 'Node') -> None:
        self.nodes.append(node_obj)
        node_obj.set_full_path(self.full_path)

    def get_node(self, path: List[str]) -> Union[Literal[False], 'Node']:
        for node in self.nodes:
            if node.name == path[0]:
                return node.get_node(path[1:])
        return False

    def flatten(self):
        flattend_list = [self]
        if self.is_expanded:
            for node in self.nodes:
                flattend_list.extend(node.flatten())

        return flattend_list

    def draw(self, pad: object, line: int, tab: str = '') -> int:
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
            line = node.draw(pad, line, tab=(tab.replace('├', '│').replace('└', ' ') + new_tab))

        return line
