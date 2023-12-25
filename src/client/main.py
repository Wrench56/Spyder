import datetime
import logging
import logging.config
import os
import getpass
import platform
import textwrap

import curses
import colorama

import yaml

from screens import chat, login

from utils import net, art, colors, constants
from structs import login_structs
import events


def main() -> None:
    colorama.init()
    setup()

    print(art.HEADER)
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        print(f'\033[31m{(" "*20+art.MOTTO)}\033[0m')
    else:
        print(' ' * 20 + art.MOTTO)
    print('=' * 40)

    infobox()
    update()

    curses.wrapper(start_curses)


def start_curses(stdscr: object) -> None:
    # Curses configuration
    curses.noecho()
    curses.mousemask(-1)
    constants.STDSCR = stdscr

    colors.init()

    login_data = login_structs.LoginData()
    login_screen = login.Login(stdscr, login_data)
    del login_screen  # Not necessarily needed

    # Open chat screen
    # TODO: Start plugin manager
    chat.Chat(stdscr)

    # Cleanup
    curses.endwin()


def infobox() -> None:
    time_ = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    user_ = getpass.getuser()
    conn_ = net.connection()
    ip = net.get_local_ip()
    plat = platform.system()
    rel = platform.release()

    print()
    print('+' + 16 * '-' + ' INFO ' + 16 * '-' + '+')
    print(f'| Time: {"".rjust(11)}{str(time_)} |')
    print(f'| User: {"".rjust(30-len(user_))}{user_} |')
    print(f'| Connection: {"".rjust(24-len(str(conn_)))}{conn_} |')
    print(f'| Local IP Address: {"".rjust(18-len(str(ip)))}{ip} |')
    print(f'| Platform: {"".rjust(26-len(plat))}{plat} |')
    print(f'|  └ Release: {"".rjust(24-len(rel))}{textwrap.shorten(rel, width=24, placeholder="...")} |')
    print(f'| {"".ljust(36)} |')
    print(f'| Version: {"".ljust(27-len(constants.VERSION))}{constants.VERSION} |')
    print('+' + 38 * '-' + '+')
    print()


def update() -> None:
    pass


def setup() -> None:
    with open('./config/logger.config.yaml', 'r', encoding='utf-8') as cfile:
        config = yaml.safe_load(cfile.read())
        logging.config.dictConfig(config)
    logging.addLevelName(logging.INFO, 'INFO ')
    logging.addLevelName(logging.WARNING, 'WARN ')
    logging.addLevelName(logging.CRITICAL, 'CRIT ')
    logging.root.addFilter(events.log.trigger)
    logging.info('Starting client...')


if __name__ == '__main__':
    main()
