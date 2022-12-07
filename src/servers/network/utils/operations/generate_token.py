import logging
import global_
from utils import token
from utils.operations import sender


def handle(client_data):
    json = client_data.new_json

    if not client_data.is_server:
        logging.warning('A non-server client tried to generate server authentication token!')
        sender.send(client_data, 'F')
        return

    username = json.get('u')
    if username is None:
        logging.warning('Group server tried to generate authentication token without providing username!')
        return

    if not global_.user_reader.is_link(username):
        token_ = token.generate()
        global_.user_reader.update_token(username, token_)
        sender.send(client_data, token_)
    else:
        logging.warning('Group server tried to generate authentication token for a link user!')
        sender.send(client_data, 'F')