import math


class Screen:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr

        self.min_width = None
        self.min_height = None

    def resize_check(self, width, height):
        if self.min_width is not None:
            if width < self.min_width:
                self.stdscr.erase()
                if width >= 20:
                    text = 'Screen too small!'
                elif width < 20 and width >= 10:
                    text = 'Too small!'
                elif width < 10 and width >= 6:
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

    def set_min(self, width, height):
        self.min_width = width
        self.min_height = height
