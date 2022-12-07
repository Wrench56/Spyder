from events import on_start

def start():
    print('Function loaded')


def init():
    on_start.subscribe(start)