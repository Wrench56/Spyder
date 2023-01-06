from abc import ABC, abstractmethod
from typing import Tuple, Callable, Optional


class Widget(ABC):
    def __init__(self, stdscr: object) -> None:
        self.stdscr = stdscr

        self.lambda_x: Callable[[int], int] = lambda x: -1
        self.lambda_y: Callable[[int], int] = lambda y: -1
        self.lambda_w: Optional[Callable[[int], int]] = None
        self.lambda_h: Optional[Callable[[int], int]] = None

        self.last_x: int = 0
        self.last_y: int = 0

    def set_size(self, lambda_x: Callable[[int], int], lambda_y: Callable[[int], int], lambda_w: Optional[Callable[[int], int]], lambda_h: Optional[Callable[[int], int]]) -> None:
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

    @abstractmethod
    def draw(self) -> None:
        pass
