# This is a workaround to solve moving the physical
# cursor on the screen. Subwindows are not capable
# of using the .move() method on themselves (actually)
# most of the time they just give you a wmove error
# without telling what is wrong. According to the
# original ncurses docs, move is a macro of wmove for
# the stdscr only, so the Python wrapper MAY be the
# cause of the bug. Without further testing I don't
# want to push the responsibility on someone else.
#
# This solution requires stdscr to be in the global
# scope, that is something I don't line, as it
# decreases Python's performance. I might change
# this in the future.


stdscr: object = None


def move(new_x: int, new_y: int) -> None:
    stdscr.move(new_y, new_x)
