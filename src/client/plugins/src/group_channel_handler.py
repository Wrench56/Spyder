from events import on_start


def start() -> None:
    print('Function loaded')


def init() -> None:
    on_start.subscribe(start)
