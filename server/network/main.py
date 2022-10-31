import logging
import logging.config
import yaml
import colorama

import keyboard
import atexit
import signal

import server

def main():
    colorama.init()

    with open('./config/logger.config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.CRITICAL, 'CRIT')
    logger = logging.getLogger()

    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    atexit.register(terminate)

    network_server = server.Server()

    print('\n          To exit the program press CTRL+Q!\n')
    keyboard.add_hotkey('ctrl+q', terminate)

    logger.info('Server starting...')
    network_server.start('0.0.0.0', 50030)

def terminate():
    atexit._run_exitfuncs()

if __name__ == '__main__':
    main()
    