import socket
import logging
from provider.encryption import asymmetric, symmetric, rndinjection as rndi

class BaseCommunicator():
    def __init__(self) -> None:
        self.fernet_key = None
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, ip, port):
        self.connect((ip, port))
        self.auth()

    def auth(self):
        self.send(b'WeAreSpyder') # magic sentence

        public_key = asymmetric.Key()
        public_key.from_bytes(self.recv(2048))

        fkey_raw = symmetric.generate()
        self.fernet_key = symmetric.convert(fkey_raw)
        self.send(asymmetric.encrypt(fkey_raw, public_key))
        
        magic_answer_encoded = self.recv(1024)
        magic_answer = rndi.decrypt(symmetric.decrypt(magic_answer_encoded, self.fernet_key).decode())
        if magic_answer != 'UnitedWeStand':
            logging.critical('Server sent wrong magic answer! Aborting...')
            return
    
    def send_encrypted(self, data):
        self.send(symmetric.encrypt(rndi.encrypt(data).encode(), self.fernet_key))
    
    def recv_encrypted(self):
        return rndi.decrypt(symmetric.decrypt(self.recv(1024), self.fernet_key).decode())