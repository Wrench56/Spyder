from typing import Callable

_subscribed = []


def subscribe(function: Callable[[], None]) -> None:
    _subscribed.append(function)


def trigger() -> None:
    for function in _subscribed:
        function()
