import logging

from encryption import symmetric, rndinjection as rndi
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

    if saved_hash is not False:
        if hash_ == saved_hash:
            logging.debug('Client provided valid credentials!')
            message = 'S'
            client_data.is_authenticated = True
        else:
            logging.warn('Client provided wrong credentials!')
            message = 'F'
            client_data.is_authenticated = False

    client_data.socket.send(symmetric.encrypt(rndi.encrypt(message).encode(), client_data.fernet_key)) # S as [S]uccess, F as [F]ailure