from widgets import widget
from utils import colors


class Label(widget.Widget):
    def __init__(self, stdscr: object, text: str) -> None:
        self.text = text
        super().__init__(stdscr)

    def draw(self) -> None:
        x, y = super().getxy()
        colors.colored_addstr(self.stdscr, self.lambda_x(x), self.lambda_y(y), self.text)

        self.stdscr.refresh()

    def set_text(self, text: str) -> None:
        self.text = text
        self.draw()
