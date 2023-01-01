# Whichkey
# A simple tool to find out what is the keycode
# of a specific (pressed) key.
# Press q to exit the program!


import curses
import math


def main(stdscr):
    y, x = stdscr.getmaxyx()
    stdscr.addstr(math.floor(y/2), math.floor((x-14)/2), 'Press any key!')
    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_RESIZE:
            stdscr.erase()
            y, x = stdscr.getmaxyx()
            stdscr.addstr(math.floor(y/2), math.floor((x-14)/2), 'Press any key!')
            stdscr.refresh()
        elif chr(ch) == 'q':
            break
        else:
            stdscr.erase()
            y, x = stdscr.getmaxyx()
            string = f'Your pressed character was: {ch}'
            stdscr.addstr(math.floor(y/2), math.floor((x-len(string))/2), string)


if __name__ == '__main__':
    curses.wrapper(main)
