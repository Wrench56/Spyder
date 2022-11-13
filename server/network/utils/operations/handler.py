import logging
from utils.operations import login, change_pw, network_name, generate_token, get_token, get_mirror


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
    elif op == 5: # Return auth token
        if client_data.is_server:
            logging.warning('Server tried to get its own authentication token, which is non-existent!')
            return
        get_token.handle(client_data)
    elif op == 6: # Get mirror (in case of a link user)
        get_mirror.handle(client_data)        
        
    


    
