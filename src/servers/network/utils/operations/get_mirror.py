import logging
import global_
from utils.operations import sender

def handle(client_data):
    json = client_data.new_json

    username = json.get('u')
    mirror_number = json.get('m')

    if not client_data.is_server:
        if username != client_data.username:
            logging.warning('A non-server client tried to get a mirror for a user!')
            return

    mirror = global_.user_reader.get_mirror(username, mirror_number)
    if mirror is None:
        sender.send(client_data, 'F') 
        return   

    sender.send(client_data, mirror)
    
    
