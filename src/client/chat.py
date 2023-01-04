from screens import chat
from plugins import handler
from events import on_start


def main(stdscr, login_data):
    handler.load_plugins()
    chat.Chat(stdscr)
    on_start.trigger()
