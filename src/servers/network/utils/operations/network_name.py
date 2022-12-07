import logging

import global_
from utils.operations import sender

def handle(client_data):
    sender.send(client_data, global_.config['network']['name'])
    logging.debug('Network name sent successfully!')