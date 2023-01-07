from typing import List, Tuple, Any, Union, Final

import curses

# First 9 numbers (1-9) are reserved for other attributes.

FG_DEFAULT = 1
BG_DEFAULT = 0

FG_BLACK = 2
FG_RED = 3
FG_GREEN = 4
FG_YELLOW = 5
FG_BLUE = 6
FG_MAGENTA = 7
FG_CYAN = 8
FG_WHITE = 9

BG_BLACK = 10
BG_RED = 20
BG_GREEN = 30
BG_YELLOW = 40
BG_BLUE = 50
BG_MAGENTA = 60
BG_CYAN = 70
BG_WHITE = 80

ANSI_COLORS = {
    '[30m': FG_BLACK,
    '[31m': FG_RED,
    '[32m': FG_GREEN,
    '[33m': FG_YELLOW,
    '[34m': FG_BLUE,
    '[35m': FG_MAGENTA,
    '[36m': FG_CYAN,
    '[37m': FG_WHITE,
    '[38m': FG_DEFAULT,  # non-ANSI option

    '[40m': BG_BLACK,
    '[41m': BG_RED,
    '[42m': BG_GREEN,
    '[43m': BG_YELLOW,
    '[44m': BG_BLUE,
    '[45m': BG_MAGENTA,
    '[46m': BG_CYAN,
    '[47m': BG_WHITE,
    '[48m': BG_DEFAULT,
}


def init() -> None:
    COLORS: Final[Tuple[Any, Any, Any, Any, Any, Any, Any, Any]] = (
        -1,  # Default
        curses.COLOR_BLACK,
        curses.COLOR_RED,
        curses.COLOR_GREEN,
        curses.COLOR_YELLOW,
        curses.COLOR_BLUE,
        curses.COLOR_MAGENTA,
        curses.COLOR_CYAN
    )
    curses.start_color()

    # Get the defaults
    curses.use_default_colors()

    for i, bg in enumerate(COLORS):
        for j, fg in enumerate(COLORS):
            curses.init_pair(i*10 + j+1, fg, bg)  # noqa: E226


def parse_ansi_string(string: str) -> List[Union[str, int]]:
    string_color_list: List[Union[str, int]] = []
    iter_string = iter(string)
    text_segment = ''
    foreground: int = FG_DEFAULT
    background: int = BG_DEFAULT
    for i, char in enumerate(iter_string):
        if char == '\x1b':
            if string[i + 2] == '3':  # foreground
                foreground = ANSI_COLORS[string[i + 1:i + 5]]
                skip = 4
            elif string[i + 2] == '4':  # background
                background = ANSI_COLORS[string[i + 1:i + 5]]
                skip = 4
            else:  # reset = 0
                foreground = FG_DEFAULT
                background = BG_DEFAULT
                skip = 3
            for _ in range(skip):
                next(iter_string)
            string_color_list.append(text_segment)
            string_color_list.append(foreground + background)

            continue

        text_segment += char
    string_color_list.append(text_segment)
    string_color_list.append(foreground + background)
    print(string_color_list)
    return string_color_list


def colored_addstr(stdscr: object, x: int, y: int, input_string: str) -> None:
    string_color_list = parse_ansi_string(input_string)
    x_shift = 0
    for i in range(0, len(string_color_list), 2):
        string = string_color_list[i]
        if string == '':
            continue
        if string_color_list[i + 1] is None:
            stdscr.addstr(y, x_shift + x, string)
        else:
            stdscr.addstr(y, x_shift + x, string, curses.color_pair(string_color_list[i + 1]))
        x_shift += len(string)  # type: ignore[arg-type]
