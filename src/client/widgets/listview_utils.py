#from utils import colors

def validate_tree(list_) -> bool:
    for i, element in enumerate(list_):
        if isinstance(element, list):
            if len(list_)-1 > i:
                if isinstance(list_[i+1], list):
                    return False
            if not validate_tree(element):
                return False
        elif isinstance(element, str) or isinstance(element, bool):
            pass
        else:
            return False
    return True

def draw_tree(pad, buffer: list, line_num: int, tab: str) -> None:
    if tab != '':
        tab_string = f'{tab}├ '
    else:
        tab_string = ''

    for i, element in enumerate(buffer):
        if isinstance(element, str):
            if len(buffer)-1 > i:
                if isinstance(buffer[i+1], list):
                    if buffer[i+1][0] is True:
                        element = '▾' + element
                    else:
                        element = '▸' + element
                    tab_string = tab_string[:-1]
                    if (len(buffer) - i) == 2:
                        tab_string = tab_string.replace('├', '└')
                if (len(buffer) - i) == 1:
                    tab_string = tab_string.replace('├', '└')
            else:
                tab_string = tab_string.replace('├', '└')
            colors.colored_addstr(pad, 0, line_num, tab_string + element)
            line_num += 1
            

        elif isinstance(element, list):
            if element[0] == True:
                if len(buffer)-1 > i and tab != '':
                    tab += '│'
                else:
                    tab += ' '
                
                line_num = draw_tree(pad, element, line_num, tab)
    return line_num

def flatten(buffer: list):
    result = []
    for element in buffer:
        if isinstance(element, list):
            if element[0]:
                result.extend(flatten(element))
        elif isinstance(element, str): # string
            result.append(element)
    
    return result

def toggle_expand(buffer: list, find_index: int, curr_index: int = 0):
    for i, element in enumerate(buffer):
        if isinstance(element, str):
            curr_index += 1
        elif isinstance(element, list):
            if element[0] == True:
                result = toggle_expand(element[1:], find_index, curr_index)
                if isinstance(result, bool):
                    return result
                else:
                    curr_index = result
        if find_index+1 == curr_index:
            if isinstance(buffer[i+1], list):
                buffer[i+1][0] = False if buffer[i+1][0] is True else True
                return True
        elif find_index+1 < curr_index:
            return False
    return curr_index

def get_list(buffer, path):
    c_path = path[0]
    for i, element in enumerate(buffer):
        if c_path == element:
            if path[-1] == c_path:
                return buffer[i+1]
            return get_list(buffer[i+1], path[1:])
    return False   


def add_node(buffer: list, name: str, path: str, subnodes: list):
    #! Only usable with positive and non-null index numbers!
    if path == '':
        buffer.append(name)
        if len(subnodes) > 0:
            buffer.append(subnodes)
        return True

    sublist = get_list(buffer, path.split('\\'))
    if sublist is False:
        return False

    sublist.append(name)
    if len(subnodes) > 0:
        sublist.append(subnodes)
    return True