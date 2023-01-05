from abc import ABC, abstractmethod

import socket
import logging
from provider.encryption import asymmetric, symmetric, rndinjection as rndi
from cryptography.fernet import Fernet


class BaseCommunicator(socket.socket, ABC):
    def __init__(self) -> None:
        self.fernet_key: Fernet
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, ip: str, port: int) -> None:
        self.connect((ip, port))
        if not self.auth():
            return
        self.login()

    def auth(self) -> bool:
        self.send(b'WeAreSpyder')  # magic sentence

        public_key = asymmetric.Key()
        public_key.from_bytes(self.recv(2048))

        fkey_raw = symmetric.generate()
        self.fernet_key = symmetric.convert(fkey_raw)
        self.send(asymmetric.encrypt(fkey_raw, public_key))

        magic_answer_encoded = self.recv(1024)
        magic_answer = rndi.decrypt(symmetric.decrypt(magic_answer_encoded, self.fernet_key).decode())
        if magic_answer != 'UnitedWeStand':
            logging.critical('Server sent wrong magic answer! Aborting...')
            return False
        return True

    def send_encrypted(self, data: str) -> None:
        self.send(symmetric.encrypt(rndi.encrypt(data).encode(), self.fernet_key))

    def recv_encrypted(self) -> str:
        return rndi.decrypt(symmetric.decrypt(self.recv(1024), self.fernet_key).decode())

    @abstractmethod
    def login(self) -> bool:
        pass
