import logging
import global_
from utils import token
from utils.operations import sender


def handle(client_data):
    json = client_data.new_json

    username = json.get('u')
    if username is None:
        logging.warning('Group server tried to generate authentication token without providing username!')
        return

    token_ = token.generate()
    global_.user_reader.update_token(username, token_)
    sender.send(client_data, token_)