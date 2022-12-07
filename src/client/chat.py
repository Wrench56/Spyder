from screens import chat
from plugins import handler
from events import on_start

def main(stdscr, login_data):
    handler.load_plugins()

    chat_screen = chat.Chat(stdscr)    
    #chat_screen.logic()
    on_start.trigger()

