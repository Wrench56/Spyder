import logging
import ipaddress

from utils.operations import sender
import global_

def handle(client_data):
    cfg = global_.config
    json = client_data.new_json


    if (json.get('s'), json.get('i'), json.get('l')).count(True) > 1:
        logging.warning('Cant\'t create multiple category user!')


    if json.get('i'): # Create invite
        if _check_policies(client_data, 'invite'):
            username, password = global_.user_reader.create_invite()
            sender.send(client_data, str({
             'u': username, 
             'p': password
            }))
        return

    if json.get('l'): # Create link
        if _check_policies(client_data, 'link'):
            mirrors = json.get('m')
            if not _validate_mirrors(mirrors):
                return

            u_ = json.get('u')
            if u_ is None or u_ == '':
                logging.warning('Link\'s username was not sent!')
                return

            global_.user_reader.create_user(u_, None, mirrors)
        return
    else: # Normal User OR Server
        u_ = json.get('u')
        if u_ is None or u_ == '':
            logging.warning('User\'s username was not sent!')
            return

        if json.get('s'): # Server
            if not _check_policies(client_data, 'server'):
                return 
            username = '__server__' + u_
        else:
            if not _check_policies(client_data, 'user'):
                return 
            username = u_

        hash_ = json.get('h')
        if hash_ is None or hash_ == '':
            logging.warning('User\'s hash was not sent!')
            return

        global_.user_reader.create_user(username, hash_)
        return
    
def _validate_mirrors(mirrors):
    if not isinstance(mirrors, list):
        logging.warning('Invalid mirror list format!')
        return False
    if len(mirrors) == 0:
        logging.warning('A client tried to create a link without any mirrors!')
        return False

    for mirror in mirrors:
        username = mirror.get('username')
        ip = mirror.get('ip')

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            logging.warning('Client provided an invalid IP!')
            return False

        if username == '' or username is None:
            logging.warning('Client provided no username!')
            return False

        return True

def _check_policies(client_data, type_):
    cfg = global_.config[type_]['create']
    status = True
    if client_data.is_user and not cfg['user']:
        status = False
    if client_data.is_server and not cfg['server']:
        status = False
    if client_data.is_link and not cfg['link']:
        status = False
    if client_data.is_invite and not cfg['invite']:
        status = False
    if not client_data.is_authenticated and not cfg['unknown']:
        status = False

    if not status:
        logging.warning('Can\'t create a new user with your current status, as policies prohibit it!')
    return status
        
        