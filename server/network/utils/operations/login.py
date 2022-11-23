import logging

from utils.operations import sender
import global_

def handle(client_data):
    json = client_data.new_json

    username = json.get('u')
    hash_ = json.get('h')
    if hash_ is None or username is None:
        logging.error('Username or password hash not provided!')
    
    reader = global_.user_reader
    if json.get('s') == True:
        username = f'__server__{username}'
        client_data.is_server = True
    else:
        client_data.is_server = False
    
    client_data.username = username
    client_data.hash_ = hash_

    saved_hash = reader.get_user_hash(username)

    message = 'F'
    if saved_hash is not False:
        if hash_ == saved_hash:
            logging.debug('Client provided valid credentials!')
            message = 'S'
            client_data.is_authenticated = True
            client_data_in_db = global_.user_reader.get_user_data(username)
            client_data.is_link = client_data_in_db.get('link') if True else False
            client_data.is_invite = client_data_in_db.get('invite') if True else False
            client_data.is_user = (not client_data.is_link and not client_data.is_invite and not client_data.is_server) if True else False
        else:
            logging.warn('Client provided wrong credentials!')
            client_data.is_authenticated = False

    sender.send(client_data, message)