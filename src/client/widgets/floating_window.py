"""This module implements a floating window widget with curses."""

from typing import Callable, Tuple, Dict
import curses

from utils import colors
from widgets import widget


class Float:
    """A floating window which does not erase the content below it."""

    def __init__(self, title: str = '') -> None:
        """
        Create the floating window without displaying it.

        Args:
            title: The title of the floating window. If the string is
                   empty, no title is displayed.
        """
        self._lambda_x: Callable[[int], int] = lambda _: 0
        self._lambda_y: Callable[[int], int] = lambda _: 0
        self._lambda_w: Callable[[int], int] = lambda _: 0
        self._lambda_h: Callable[[int], int] = lambda _: 0

        self._last_x = 0
        self._last_y = 0
        self.left_title_wrapping: str = ' '
        self.right_title_wrapping: str = ' '
        self.title = title

        self._widgets: Dict[str, widget.Widget] = {}

        self._window = curses.newwin(1, 1, 0, 0)

    def add_widget(self, name: str, widget_: widget.Widget) -> None:
        """
        Add a widget to the floating window without refreshing it.

        Args:
            name: The name of the new widget which will be used later
                  to access it when needed. If the specified name
                  already exists in the widgets list, the widget won't
                  be added.
            widget_: The widget itself. It has to be a child of
                     Widget()
        """
        if name not in self._widgets:
            self._widgets[name] = widget_

    def set_size(self, lambda_x: Callable[[int], int], lambda_y: Callable[[int], int], lambda_w: Callable[[int], int], lambda_h: Callable[[int], int]) -> None:
        """
        Specify the responsive size of the window with lambda functions.

        Args:
            lambda_x: A lambda function defining the upper left
                      corner's x coordinate with the width of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
            lambda_y: A lambda function defining the upper left
                      corner's y coordinate with the height of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
            lambda_w: A lambda function defining the bottom right
                      corner's x coordinate with the width of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
            lambda_h: A lambda function defining the bottom right
                      corner's y coordinate with the height of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
        """
        self._lambda_x = lambda_x
        self._lambda_y = lambda_y
        self._lambda_w = lambda_w
        self._lambda_h = lambda_h

    def _getxy(self) -> Tuple[int, int]:
        return self._last_x, self._last_y

    def resize(self, x: int, y: int) -> None:
        """
        Resize the floating window with respect to the parent's \
        x and y coordinates.

        Args:
            x: Parent window's width (bottom right corner's x)
            y: Parent window's height (bottom right corner's y)
        """
        self._last_x = x
        self._last_y = y

        self.draw()

    def draw(self) -> None:
        """Draw the window and all widgets on it."""
        x, y = self._getxy()
        width = self._lambda_w(x)
        height = self._lambda_h(y)

        self._window.mvwin(self._lambda_y(y), self._lambda_x(x))
        self._window.resize(height, width)

        y, x = self._window.getyx()
        for widget_ in self._widgets.values():
            widget_.resize(width, height)

        self._window.box()
        if self.title:
            colors.colored_addstr(self._window, 2, 0, f'{self.left_title_wrapping}{self.title}{self.right_title_wrapping}')
        self._window.refresh()

    def get(self) -> object:
        """
        Return the curses window object.

        Returns:
            object: The curses window object of the floating window
        """
        return self._window
