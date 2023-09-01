from typing import Callable, Tuple, Dict
import curses

from utils import colors
from widgets import widget


class Float:
    def __init__(self, title: str = '') -> None:
        self.lambda_x: Callable[[int], int] = lambda _: 0
        self.lambda_y: Callable[[int], int] = lambda _: 0
        self.lambda_w: Callable[[int], int] = lambda _: 0
        self.lambda_h: Callable[[int], int] = lambda _: 0

        self.last_x = 0
        self.last_y = 0
        self.left_title_wrapping: str = ' '
        self.right_title_wrapping: str = ' '
        self.title = title

        self.widgets: Dict[str, widget.Widget] = {}

        self.window = curses.newwin(1, 1, 0, 0)

    def add_widget(self, name: str, widget_: widget.Widget) -> None:
        if name not in self.widgets:
            self.widgets[name] = widget_

    def set_size(self, lambda_x: Callable[[int], int], lambda_y: Callable[[int], int], lambda_w: Callable[[int], int], lambda_h: Callable[[int], int]) -> None:
        self.lambda_x = lambda_x
        self.lambda_y = lambda_y
        self.lambda_w = lambda_w
        self.lambda_h = lambda_h

    def getxy(self) -> Tuple[int, int]:
        return self.last_x, self.last_y

    def resize(self, x: int, y: int) -> None:
        self.last_x = x
        self.last_y = y

        self.draw()

    def draw(self) -> None:
        x, y = self.getxy()
        width = self.lambda_w(x)
        height = self.lambda_h(y)

        self.window.mvwin(self.lambda_y(y), self.lambda_x(x))
        self.window.resize(height, width)

        y, x = self.window.getyx()
        for widget_ in self.widgets.values():
            widget_.resize(width, height)

        self.window.box()
        if self.title:
            colors.colored_addstr(self.window, 2, 0, f'{self.left_title_wrapping}{self.title}{self.right_title_wrapping}')
        self.window.refresh()

    def get(self) -> object:
        return self.window
