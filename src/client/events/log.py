from typing import List, Callable
import logging

_subscribed: List[Callable[[logging.LogRecord], None]] = []


def subscribe(function: Callable[[logging.LogRecord], None]) -> None:
    _subscribed.append(function)


def unsubscribe(function: Callable[[logging.LogRecord], None]) -> None:
    del _subscribed[_subscribed.index(function)]  # KeyError: function was not subscribed


# This should not be called by anything except the logging library
# Return a bool to satisfy logging.root.addFilter() requirements
def trigger(record: logging.LogRecord) -> bool:
    for function in _subscribed:
        function(record)

    return True
