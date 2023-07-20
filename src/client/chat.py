from screens import chat
import events
from plugins import handler


def main(stdscr: object, _: object) -> None:
    handler.load_plugins()
    chat.Chat(stdscr)
    events.start.trigger()
