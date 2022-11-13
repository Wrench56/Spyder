import json
import logging

#! This class should be changed relatively soon, as it is killing the memory

class Reader():
    def __init__(self, path):
        self.path = path

        self.buffer = {}

    def open(self):
        with open(self.path, 'r') as f:
            self.buffer = json.load(f)
            f.close()

class UserReader(Reader):
    def __init__(self, path):
        super().__init__(path)
    
    def get_user_hash(self, username, log=True):
        for user_entry in self.buffer.get('users'):
            if user_entry.get('username') == username:
                return user_entry.get('hash')
        
        if log: # When called from create_user(), we don't want to receive any warning
            logging.warning('Username not found in system! This might be an attack attempt!')   
        return False

    def create_user(self, username: str, hash_):
        if self.get_user_hash(username, log=False) is not False:
            logging.warning('User already exists!')
            return False

        self.buffer.get('users').append({
            'username': username,
            'hash': hash_
        })
        self.write()

        return True

    def update_field(self, username, field, new_value, log_string):
        entry_index = None
        
        for i, user_entry in enumerate(self.buffer.get('users')):
            if user_entry.get('username') == username:
                entry_index = i

        if entry_index is None:
            logging.warning(f'User does not exits! Can\'t change {log_string}!')
            return False

        self.buffer['users'][entry_index][field] = new_value
        self.write()
        logging.debug(f'Client changed {log_string} successfully!')

        return True
        
    def update_password(self, username, new_hash):
        return self.update_field(username, 'hash', new_hash, log_string='password hash')

    def update_token(self, username, token):
        return self.update_field(username, 'token', token, log_string='authentication token')

    def get_user_field(self, username, field, log_string):
        entry_index = None
        
        for i, user_entry in enumerate(self.buffer.get('users')):
            if user_entry.get('username') == username:
                entry_index = i

        if entry_index is None:
            logging.warning(f'User does not exits! Can\'t return {log_string}!')
            return False

        return self.buffer['users'][entry_index][field]

    def is_link(self, username):
        is_link = 0
        for user_entry in self.buffer.get('users'):
            if user_entry.get('username') == username:
                is_link = user_entry.get('link')        
        
        if is_link == 0:
            logging.warning(f'User does not exits! Can\'t tell if user {username} is a link!')

        if is_link is not True:
            return False
        return True

    def get_mirror(self, username, number):
        mirrors = []
        for user_entry in self.buffer.get('users'):
            if user_entry.get('username') == username:
                mirrors = user_entry.get('mirrors')        
        
        if len(mirrors) == 0:
            logging.warning(f'User does not exits or it has no mirrors! Can\'t return the mirrors of user {username}!')
            return None
        
        try:
            return mirrors[number]
        except IndexError:
            logging.warning(f'User {username} does not have a {number}. mirror!')
            return None
        

    def write(self):
        with open(self.path, 'w') as f:
            json.dump(self.buffer, f)
            f.close()
        
        return True