import events


def start() -> None:
    print('Function loaded')


def init() -> None:
    events.start.subscribe(start)
