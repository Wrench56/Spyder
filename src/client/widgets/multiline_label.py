from utils import colors
from widgets.label import Label


class MultilineLabel(Label):
    def draw(self) -> None:
        x, y = super().getxy()
        for i, line in enumerate(self.text.split('\n')):
            colors.colored_addstr(self.stdscr, self.lambda_x(x), self.lambda_y(y) + i, str(line))

        self.stdscr.refresh()
