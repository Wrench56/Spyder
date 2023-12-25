# This is a workaround to solve moving the physical
# cursor on the screen. Subwindows are not capable
# of using the .move() method on themselves (actually)
# most of the time they just give you a wmove error
# without telling what is wrong. According to the
# original ncurses docs, move is a macro of wmove for
# the stdscr only, so the Python wrapper MAY be the
# cause of the bug. Without further testing I don't
# want to push the responsibility on someone else.

from utils import constants


def move(new_x: int, new_y: int) -> None:
    constants.STDSCR.move(new_y, new_x)
