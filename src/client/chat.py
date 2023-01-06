from screens import chat
from events import on_start
from plugins import handler


def main(stdscr: object, _: object) -> None:
    handler.load_plugins()
    chat.Chat(stdscr)
    on_start.trigger()
