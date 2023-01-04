from utils.colors import colored_addstr


class Node:
    def __init__(self, name: str, nodes: list = [], is_expanded: bool = True) -> None:
        self.name: str = name

        self.nodes: list = nodes
        self.is_expanded: bool = is_expanded

    def toggle_state(self):
        if len(self.nodes) > 0:
            self.is_expanded = False if self.is_expanded else True
            return True
        return False

    def add_node(self, node_obj: object):
        self.nodes.append(node_obj)

    def get_node(self, path: list):
        for node in self.nodes:
            if node.name == path[0]:
                return node.get_node(path[1:])
        return False

    def get_by_index(self, f_index: int, c_index: int, path: str = ''):
        path += self.name
        c_index += 1
        if c_index == f_index:
            if len(self.nodes) > 0:
                self.toggle_state()
                return self.is_expanded
            return path

        if self.is_expanded:
            path += '/'
            for node in self.nodes:
                result = node.get_by_index(f_index, c_index, path)
                if isinstance(result, bool) or isinstance(result, str):
                    return result

                c_index = result
        return c_index

    def draw(self, pad, line: int, tab: str = ''):
        if len(self.nodes) > 0:
            if self.is_expanded:
                ec_char = '▾'
            else:
                ec_char = '▸'
        else:
            ec_char = '╴'
        colored_addstr(pad, 0, line, f'{tab}{ec_char}{self.name}')
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
