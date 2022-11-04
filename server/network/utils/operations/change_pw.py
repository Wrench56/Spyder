import global_

def handle(client_data):
    reader = global_.user_reader
    reader.update_password(client_data.username, client_data.new_json.get('h'))
