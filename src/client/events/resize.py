import logging
from typing import Callable, List

# pylint: disable=broad-exception-caught

_subscribed: List[Callable[[int, int], None]] = []


def subscribe(function: Callable[[int, int], None]) -> None:
    _subscribed.append(function)


def unsubscribe(function: Callable[[int, int], None]) -> None:
    try:
        del _subscribed[_subscribed.index(function)]
    except KeyError:
        logging.error(f'Function {function} wants to unsubscribe but it is not on the subscribed list')


def trigger(x_max: int, y_max: int) -> None:
    for function in _subscribed:
        try:
            function(x_max, y_max)
        except Exception as error:
            logging.error(f'Unexpected error "{error}" when triggering subscribed function {function}')
