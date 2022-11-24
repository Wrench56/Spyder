import global_
from utils.operations import sender

def handle(client_data):
    reader = global_.user_reader
    new_username = client_data.new_json.get('u')
    if client_data.is_server:
        new_username = f'__server__{new_username}'

    if reader.update_username(client_data.username, new_username) is True:
        sender.send(client_data, 'S')
    else:
        sender.send(client_data, 'F')