_subscribed = []

def subscribe(function):
    _subscribed.append(function)

def trigger(x_max, y_max):
    for function in _subscribed:
        function(x_max, y_max)