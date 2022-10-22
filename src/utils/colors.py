import curses

BLACK_ON_BLACK = 1
BLUE_ON_BLACK = 2
GREEN_ON_BLACK = 3
RED_ON_BLACK = 4
YELLOW_ON_BLACK = 5
WHITE_ON_BLACK = 6



def init():
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK) # Am I going to use this anytime?
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)