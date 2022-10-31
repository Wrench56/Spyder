import socket
import logging
from client.encryption import asymmetric, symmetric, rndinjection as rndi

class Client(socket.socket):
    def __init__(self) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, ip, port):
        self.connect((ip, port))
        self.login()

    def login(self):
        self.send(b'WeAreSpyder')

        public_key = asymmetric.Key()
        public_key.from_bytes(self.recv(2048))

        fkey_raw = symmetric.generate()
        fernet_key = symmetric.convert(fkey_raw)
        self.send(asymmetric.encrypt(fkey_raw, public_key))
        
        magic_answer_encoded = self.recv(1024)
        magic_answer = rndi.decrypt(symmetric.decrypt(magic_answer_encoded, fernet_key).decode())
        if magic_answer != 'UnitedWeStand-':
            logging.critical('Server sent wrong magic answer! Aborting...')

