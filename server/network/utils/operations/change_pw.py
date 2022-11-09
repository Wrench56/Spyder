import global_
from utils.operations import sender

def handle(client_data):
    reader = global_.user_reader
    if reader.update_password(client_data.username, client_data.new_json.get('h')) is True:
        sender.send(client_data, 'S')
    else:
        sender.send(client_data, 'F')