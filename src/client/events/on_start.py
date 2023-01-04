_subscribed = []


def subscribe(function):
    _subscribed.append(function)


def trigger():
    for function in _subscribed:
        function()
