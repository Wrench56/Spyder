from typing import List, Callable

_subscribed: List[Callable[[int, int], None]] = []


def subscribe(function: Callable[[int, int], None]) -> None:
    _subscribed.append(function)


def unsubscribe(function: Callable[[int, int], None]) -> None:
    del _subscribed[_subscribed.index(function)]  # KeyError: function was not subscribed


def trigger(x_max: int, y_max: int) -> None:
    for function in _subscribed:
        function(x_max, y_max)
