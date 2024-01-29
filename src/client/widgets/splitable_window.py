from typing import Callable

from widgets import floating_window


class SplitWindow(floating_window.Float):
    """A window which can be split into multiple children."""

    def __init__(self) -> None:
        self._children = []
        super().__init__('', True)

    def draw(self) -> None:
        """Draw the window."""
        x, y = super()._getxy()
        super().draw()

        # TODO: Find a smart way to not call this twice
        x, y = super()._getxy()
        for child in self._children:
            child.resize(x, y)

    def split_horizontal(self, width: Callable[int, [int]], left: bool = True) -> 'SplitWindow':
        """
        Split window horizontally.

        Args:
            width: A lambda function defining the width of the
                   child window. Input is max width of the parent
            left: Whether to split from the left or right of the parent
                  window"""
        child = SplitWindow()
        x, y = super()._getxy()

        # TODO: Find a smarter way to deep copy lambdas
        self._lambda_w = lambda w, prev_w=self._lambda_w, child_w=width: prev_w(w) - child_w(w)
        if left:
            child.set_size(lambda x, prev_x=self._lambda_x: prev_x(x), lambda y, prev_y=self._lambda_y: prev_y(y), width, lambda h, prev_h=self._lambda_h: prev_h(h))
            self._lambda_x = lambda x, prev_x=self._lambda_x, child_w=width: prev_x(x) + child_w(x)
        else:
            child.set_size(lambda x, prev_x=self._lambda_x, prev_w=self._lambda_w: prev_x(x) + prev_w(x), lambda y, prev_y=self._lambda_y: prev_y(y), width, lambda h, prev_h=self._lambda_h: prev_h(h))

        self._children.append(child)
        self.draw()

        return child

    def split_vertical(self, height: Callable[int, [int]], top: bool = True) -> 'SplitWindow':
        """
        Split window vertically.

        Args:
            height: A lambda function defining the height of the
                    child window. Input is max height of the parent
                    window
            top: Whether to split from the top or bottom of the parent
                 window
        """
        child = SplitWindow()
        x, y = super()._getxy()

        # TODO: Find a smarter way to deep copy lambdas
        self._lambda_h = lambda h, prev_h=self._lambda_h, child_h=height: prev_h(h) - child_h(h)
        if top:
            child.set_size(lambda x, prev_x=self._lambda_x: prev_x(x), lambda y, prev_y=self._lambda_y: prev_y(y), lambda w, prev_w=self._lambda_w: prev_w(w), height)
            self._lambda_y = lambda h, prev_y=self._lambda_y, child_h=height: prev_y(h) + child_h(h)
        else:
            child.set_size(lambda x, prev_x=self._lambda_x: prev_x(x), lambda y, prev_y=self._lambda_y, prev_h=self._lambda_h: prev_y(y) + prev_h(y), lambda w, prev_w=self._lambda_w: prev_w(w), height)

        self._children.append(child)
        self.draw()

        return child
