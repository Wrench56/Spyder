"""This module implements the abstract widget class."""

from abc import ABC, abstractmethod
from typing import Tuple, Callable, Optional


class Widget(ABC):
    """
    The abstract widget class.

    Implements a basic __init__ method, a set_size method (although
    lambda_w and lambda_h are optional), getxy method, resize method
    and forces the developer to implement abstract method draw.
    """

    def __init__(self, stdscr: object) -> None:
        """Create the widget and initialize some variables."""
        self.stdscr = stdscr

        self.lambda_x: Callable[[int], int] = lambda x: -1
        self.lambda_y: Callable[[int], int] = lambda y: -1
        self.lambda_w: Optional[Callable[[int], int]] = None
        self.lambda_h: Optional[Callable[[int], int]] = None

        self.last_x: int = 0
        self.last_y: int = 0

    def set_size(self, lambda_x: Callable[[int], int], lambda_y: Callable[[int], int], lambda_w: Optional[Callable[[int], int]], lambda_h: Optional[Callable[[int], int]]) -> None:
        """
        Specify the responsive size of the widget with lambda functions.

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
                      This lambda function is not required for some
                      widgets, like label. Provide None if not needed
            lambda_h: A lambda function defining the bottom right
                      corner's y coordinate with the height of the
                      parent window as input. The return value has to
                      be a positive integer which fits in the
                      boundaries defined by the parent window.
                      This lambda function is not required for some
                      widgets, like label. Provide None if not needed
        """
        self.lambda_x = lambda_x
        self.lambda_y = lambda_y
        self.lambda_w = lambda_w
        self.lambda_h = lambda_h

    def getxy(self) -> Tuple[int, int]:
        return self.last_x, self.last_y

    def resize(self, x: int, y: int) -> None:
        """
        Resize the widget.

        Args:
            x: Parent window's width (bottom right corner's x)
            y: Parent window's height (bottom right corner's y)
        """
        self.last_x = x
        self.last_y = y

        self.draw()

    @abstractmethod
    def draw(self) -> None:
        """
        Draw the widget.

        You have to implement this method for each and every unique
        widget.
        """
        pass
