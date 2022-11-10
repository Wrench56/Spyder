import logging
import logging.config
import yaml
import colorama

import keyboard
import atexit
import signal

import server
import global_
from data import reader

def main():
    colorama.init()

    with open('./config/logger.config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        f.close()
    logging.addLevelName(logging.INFO, 'INFO ')
    logging.addLevelName(logging.WARNING, 'WARN ')
    logging.addLevelName(logging.CRITICAL, 'CRIT ')

    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    atexit.register(terminate)

    network_server = server.Server()

    print('\n\n                  To exit the program press CTRL+Q!\n\n')
    keyboard.add_hotkey('ctrl+q', terminate)

    print('        Time        |        Module        |  Level     Description')
    print('                    |                      |                       ')

    logging.info('Setting up JSON database readers!')
    global_.user_reader = reader.UserReader('./data/json/users.json')
    global_.user_reader.open()

    logging.info('Loading configuration file!')
    with open('./config/config.yaml') as f:
        global_.config = yaml.safe_load(f)
        f.close()
    logging.getLogger().setLevel(global_.config['debug']['level'])

    logging.info('Server starting...')
    network_server.start('0.0.0.0', 50030)

def terminate():
    atexit._run_exitfuncs()

if __name__ == '__main__':
    main()
    