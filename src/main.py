import colorama
from termcolor import colored
import art
import datetime
import os
import platform
import curses

from screens import login

from utils import net
import data

VERSION = '0.1.0'

def main(stdscr):
    header = art.text2art('Spyder')

    print(header)
    print(colored(' '*20+'Chatting safely!', 'red'))
    print('='*40)

    infobox()
    update()
    
    curses.noecho()

    login_data = data.DataObject() 

    login_screen = login.Login(stdscr, login_data)
    login_screen.show()


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