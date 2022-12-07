import logging
import global_
from utils.operations import sender

def handle(client_data):
    if client_data.is_server:
        logging.warning('Group server tried to get its own authentication token, which is non-existent!')
        sender.send(client_data, 'F')
        return

    token = global_.user_reader.get_user_data(client_data.username)['token']
    if token is not None:
        sender.send(client_data, token)
    logging.debug('Authentication token sent successfully!')