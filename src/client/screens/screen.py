from typing import Optional

import math


class Screen:
    def __init__(self, stdscr: object) -> None:
        self.stdscr = stdscr

        self.min_width: Optional[int] = None
        self.min_height: Optional[int] = None

    def resize_check(self, width: int, height: int) -> bool:
        if self.min_width is not None:
            if width < self.min_width:
                self.stdscr.erase()
                if width >= 20:
                    text = 'Screen too small!'
                elif 20 > width >= 10:
                    text = 'Too small!'
                elif 10 > width >= 6:
                    text = 'Small'  # Might not be needed, some OS does not even allow so small windows
                self.stdscr.addstr(math.floor(height / 2), math.floor((width - len(text)) / 2), text)
                self.stdscr.refresh()

                return False
        if self.min_height is not None:
            if height < self.min_height:
                self.stdscr.erase()
                text = 'Screen too small!'
                self.stdscr.addstr(math.floor(height / 2), math.floor((width - len(text)) / 2), text)
                self.stdscr.refresh()

                return False

        return True

    def set_min(self, width: int, height: int) -> None:
        self.min_width = width
        self.min_height = height
