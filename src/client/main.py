import colorama
import datetime
import os
import platform
import curses
import logging
import logging.config
import yaml

from screens import login
import chat

from utils import net, art, colors, cursor
from data.structs import login_structs

VERSION = '0.1.0'


def main(stdscr):
    setup()

    # Create color pairs

    print(art.HEADER)
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        print(f'\033[31m{(" "*20+art.MOTTO)}\033[0m')
    else:
        print(" " * 20 + art.MOTTO)
    print('=' * 40)

    infobox()
    update()

    # Curses configuration
    curses.noecho()
    curses.mousemask(-1)
    cursor.stdscr = stdscr

    colors.init()

    login_data = login_structs.LoginData()
    login_screen = login.Login(stdscr, login_data)
    del login_screen  # Not necessarily needed

    chat.main(stdscr, login_data)

    curses.endwin()


def infobox():
    time_ = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    user_ = os.popen('whoami').read().replace('\n', '')
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
    print(f'|  └  Release: {"".rjust(23-len(rel))}{rel} |')
    print(f'| {"".ljust(36)} |')
    print(f'| Version: {"".ljust(27-len(VERSION))}{VERSION} |')
    print('+' + 38 * '-' + '+')
    print()


def update():
    pass


def setup():
    with open('./config/logger.config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logging.addLevelName(logging.INFO, 'INFO ')
    logging.addLevelName(logging.WARNING, 'WARN ')
    logging.addLevelName(logging.CRITICAL, 'CRIT ')
    logging.info('Starting client...')


if __name__ == '__main__':
    colorama.init()
    setup()
    curses.wrapper(main)
