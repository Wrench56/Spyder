import logging
from pydoc import cli
from utils.operations import login, change_pw, network_name, generate_token


def handle_operation(client_data) -> bool|None: 
    json = client_data.new_json
    op = json.get('o')
    
    if not client_data.is_authenticated and op != 1:
        logging.warning('Client wanted to perform an auth required task without authentication!')
        return

    if op is None:
        logging.error('Operation JSON does not contain operation number!')
    elif op == 1: # Login
        login.handle(client_data)
    elif op == 2: # Network name
        network_name.handle(client_data)
    elif op == 3: # Change password
        change_pw.handle(client_data)
    elif op == 4: # Generate tokens
        if not client_data.is_server:
            logging.warning('A non-server client tried to generate server authentication token!')
            return
        generate_token.handle(client_data)
        
    


    
