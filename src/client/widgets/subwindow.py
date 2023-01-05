import curses

from widgets import widget


class Subwindow(widget.Widget):
    def __init__(self, stdscr: object, border: bool = True):
        self.border: bool = border
        self.window: object = stdscr.subwin(0, 0)
        super().__init__(stdscr)

    def draw(self) -> None:
        x, y = super().getxy()

        # I have no idea why the previous version failed, but this is working pretty well!
        try:  # ! Do NOT delete this: this saves you from a lot of curses error
            self.window.resize(1, 1)
            self.window.mvwin(0, 0)
        except curses.error:
            self.window.mvwin(0, 0)
            self.window.resize(1, 1)

        self.window.mvwin(self.lambda_y(y), self.lambda_x(x))
        self.window.resize(self.lambda_h(y), self.lambda_w(x))
        if self.border:
            self.window.border(0)
        self.window.refresh()

    def get(self) -> object:
        return self.window
