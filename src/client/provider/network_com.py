import logging
from time import sleep
import json

import base_com


class NetworkCommunicator(base_com.BaseCommunicator):
    WAIT_BETWEEN_MESSAGES = 0.0000000001

    def __init__(self) -> None:
        super().__init__()

    def login(self):
        login_json = {
            'o': 1,         # [1. Operation] - Login
            's': False,     # [Server] - False
            'u': 'wrench',  # [Username] - wrench
            'h': 'ABCD'     # [Hash] - ABCD
        }
        self.send_encrypted(json.dumps(login_json))
        sleep(self.WAIT_BETWEEN_MESSAGES)
        if self.recv_encrypted() == 'F':
            logging.critical('Could not log in to network server! Did your password hash change?')
