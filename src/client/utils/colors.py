from typing import List, Union

import curses

BLACK_ON_BLACK = 1
RED_ON_BLACK = 2
GREEN_ON_BLACK = 3
YELLOW_ON_BLACK = 4
BLUE_ON_BLACK = 5
MAGENTA_ON_BLACK = 6
CYAN_ON_BLACK = 7
WHITE_ON_BLACK = 8

BLACK_ON_WHITE = 71

ANSI_COLORS = {
    '[30m': BLACK_ON_BLACK,
    '[31m': RED_ON_BLACK,
    '[32m': GREEN_ON_BLACK,
    '[33m': YELLOW_ON_BLACK,
    '[34m': BLUE_ON_BLACK,
    '[35m': MAGENTA_ON_BLACK,
    '[36m': CYAN_ON_BLACK,
    '[37m': WHITE_ON_BLACK,
    '[0m': None
}


def init() -> None:
    curses.start_color()

    curses.init_pair(BLACK_ON_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)  # Am I going to use this anytime?
    curses.init_pair(RED_ON_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(GREEN_ON_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(YELLOW_ON_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(BLUE_ON_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(MAGENTA_ON_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(CYAN_ON_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(WHITE_ON_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.init_pair(BLACK_ON_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)


def parse_ansi_string(string: str) -> List[Union[str, int, None]]:
    string_color: List[Union[str, int, None]] = []
    iter_string = iter(string)
    text = ''
    color = None
    char_number = 0
    for char in iter_string:
        if char == '\x1b':
            string_color.append(text)
            string_color.append(color)
            text = ''
            ansi_esc = string[char_number + 1:char_number + 4]
            if ansi_esc[-2] != '0':
                ansi_esc = ansi_esc + string[char_number + 4]
            color = ANSI_COLORS[ansi_esc]

            for _ in range(len(ansi_esc)):
                next(iter_string)
            char_number += len(ansi_esc) + 1
            continue

        text += char
        char_number += 1
    string_color.append(text)
    string_color.append(color)
    return string_color


def colored_addstr(stdscr: object, x: int, y: int, input_string: str) -> None:
    string_color = parse_ansi_string(input_string)
    x_shift = 0
    for i in range(0, len(string_color), 2):
        string = string_color[i]
        if string == '':
            continue
        if string_color[i + 1] is None:
            stdscr.addstr(y, x_shift + x, string)
        else:
            stdscr.addstr(y, x_shift + x, string, curses.color_pair(string_color[i + 1]))
        x_shift += len(string)  # type: ignore[arg-type]
