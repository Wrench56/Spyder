import logging
from typing import Callable, List

# pylint: disable=broad-exception-caught

_subscribed: List[Callable[[logging.LogRecord], None]] = []


def subscribe(function: Callable[[logging.LogRecord], None]) -> None:
    _subscribed.append(function)


def unsubscribe(function: Callable[[logging.LogRecord], None]) -> None:
    try:
        del _subscribed[_subscribed.index(function)]
    except KeyError:
        logging.error(f'Function {function} wants to unsubscribe but it is not on the subscribed list')


# This should not be called by anything except the logging library
# Return a bool to satisfy logging.root.addFilter() requirements
def trigger(record: logging.LogRecord) -> bool:
    for function in _subscribed:
        try:
            function(record)
        except Exception as error:
            # Disable log event callback
            logging.root.removeFilter(trigger)
            logging.error(f'Unexpected error "{error}" when triggering subscribed function {function}')
            logging.root.addFilter(trigger)
    return True
