import colorama
from termcolor import colored
import datetime
import os
import platform
import curses

from screens import login

from utils import net, art, colors
import data

VERSION = '0.1.0'

def main(stdscr):
    # Create color pairs

    print(art.HEADER)
    print(colored(' '*20+art.MOTTO, 'red'))
    print('='*40)

    infobox()
    update()
    
    curses.noecho()

    colors.init()

    login_data = data.DataObject() 

    login_screen = login.Login(stdscr, login_data)


    curses.endwin()

def infobox():
    time_ = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    user_ = os.popen('whoami').read().replace('\n', '')
    conn_ = net.connection()
    ip = net.get_local_ip()
    plat = platform.system()
    rel = platform.release()

    print()
    print('+' + 16*'-' + ' INFO ' + 16*'-' + '+')
    print(f'| Time: {"".rjust(11)}{str(time_)} |')
    print(f'| User: {"".rjust(30-len(user_))}{user_} |')
    print(f'| Connection: {"".rjust(24-len(str(conn_)))}{conn_} |')
    print(f'| Local IP Address: {"".rjust(18-len(str(ip)))}{ip} |')
    print(f'| Platform: {"".rjust(26-len(plat))}{plat} |')
    print(f'|  └  Release: {"".rjust(23-len(rel))}{rel} |')
    print(f'| {"".ljust(36)} |')
    print(f'| Version: {"".ljust(27-len(VERSION))}{VERSION} |')
    print('+' + 38*'-' + '+')
    print()

def update():
    pass

if __name__ == '__main__':
    colorama.init()

    curses.wrapper(main)