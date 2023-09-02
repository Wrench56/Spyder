"""
This module implements subwindows.

Subwindows are windows that can be updated separately from the
main (stdscr) window. The difference between subwindows and regular
windows is, that regular windows don't erase the area under them. This
of course means, that the window below them has to keep the drawn area
in memory. When a subwindow is created, the parent window does not care
about that area anymore and thus this leads for smaller memory
footprint. For separating a window into smaller sections, subwindows
are the perfect solution. Use regular windows however, to create popups
or anything stacked over the regular window layer without erasing the
content below them.
"""

import curses

from widgets import widget


class Subwindow(widget.Widget):
    """A subwindow used to separate windows in smaller sections."""

    def __init__(self, stdscr: object, border: bool = True) -> None:
        """
        Create the subwindow without displaying it.

        Args:
            stdscr: The parent window object (curses window)
            border: Whether to draw a border around the subwindow
                    or not. True by default
        """
        self.border: bool = border
        self.window: object = stdscr.subwin(0, 0)
        super().__init__(stdscr)

    def draw(self) -> None:
        """Draw the subwindow."""
        x, y = super().getxy()

        # I have no idea why the previous version failed, but this is working pretty well!
        try:  # ! Do NOT delete this: this saves you from a lot of curses error
            self.window.resize(1, 1)
            self.window.mvwin(0, 0)
        except curses.error:
            self.window.mvwin(0, 0)
            self.window.resize(1, 1)

        self.window.mvwin(self.lambda_y(y), self.lambda_x(x))
        self.window.resize(self.lambda_h(y), self.lambda_w(x))  # type: ignore[misc]
        if self.border:
            self.window.border(0)
        self.window.refresh()

    def get(self) -> object:
        """
        Return the curses subwindow object.

        Returns:
            object: The curses window object of the subwindow
        """
        return self.window
