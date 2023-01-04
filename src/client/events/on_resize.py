_subscribed = []


def subscribe(function):
    _subscribed.append(function)


def unsubscribe(function):
    del _subscribed[_subscribed.index(function)]  # KeyError: function was not subscribed


def trigger(x_max, y_max):
    for function in _subscribed:
        function(x_max, y_max)
