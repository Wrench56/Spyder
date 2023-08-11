import logging
from typing import Callable, List

# pylint: disable=broad-exception-caught

_subscribed: List[Callable[[], bool]] = []


def subscribe(function: Callable[[], bool]) -> None:
    _subscribed.append(function)


def unsubscribe(function: Callable[[], bool]) -> None:
    try:
        del _subscribed[_subscribed.index(function)]
    except KeyError:
        logging.error(f'Function {function} wants to unsubscribe but it is not on the subscribed list')


def trigger() -> None:
    for function in _subscribed:
        try:
            function()
        except Exception as error:
            logging.error(f'Unexpected error "{error}" when triggering subscribed function {function}')
