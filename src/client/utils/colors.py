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


def init():
    curses.start_color()

    curses.init_pair(BLACK_ON_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK) # Am I going to use this anytime?
    curses.init_pair(RED_ON_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(GREEN_ON_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(YELLOW_ON_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(BLUE_ON_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(MAGENTA_ON_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(CYAN_ON_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(WHITE_ON_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.init_pair(BLACK_ON_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)

def parse_ansi_string(string):
        string_color = []
        iter_string = iter(string)
        text = ''
        color = None
        char_number = 0
        for char in iter_string:
            if char == '\x1b':
                string_color.append(text)
                string_color.append(color)
                text = ''
                color = ANSI_COLORS[string[char_number+1:char_number+5]]
                for _ in range(4):
                    next(iter_string)
                char_number += 5
                continue

            text += char
            char_number += 1
        string_color.append(text)
        string_color.append(color)
        if string_color[0] == '':
            del string_color[0:2]

        return tuple(string_color)

def colored_addstr(stdscr, x, y, string):
    string_color = parse_ansi_string(string)
    for i in range(len(string_color), step=2):
        if string_color[i+1] == None:
            stdscr.addstr(y, x, string_color[i+1])
        else:
            stdscr.addstr(y, x, string_color[i+1], string_color[i+1])
