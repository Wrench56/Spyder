from widgets import widget

class Subwindow(widget.Widget):
    def __init__(self, stdscr, border=True):
        self.window = stdscr.subwin(0, 0)
        super().__init__(stdscr)

    def draw(self):
        x, y = super().getxy()

        self.window.resize(1, 1)
        self.window.mvwin(self.lambda_y(y), self.lambda_x(x))
        self.window.resize(self.lambda_h(x), self.lambda_w(x))
        self.window.border(0)
        self.window.refresh()

    def get(self):
        return self.window

