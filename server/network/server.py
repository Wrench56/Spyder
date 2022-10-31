import socket
import atexit
import logging

from encryption import symmetric, asymmetric, rndinjection as rndi
from utils import memory, threads

class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.threads = []
        self.run = True

        atexit.register(self.cleanup)

    def start(self, ip, port):
        self.bind((ip, port))

        accept_new_thread = threads.DestroyableThread(target=self.accept_new)
        accept_new_thread.setName('AcceptNewUserThread')
        self.threads.append(accept_new_thread)
        accept_new_thread.start()
    
    def accept_new(self):
        while self.run:
            self.listen()
            try:
                conn, _ = self.accept()
                new_user_thread = threads.SocketThread(target=self.handle_login, args=(conn,))
                new_user_thread.setName(f'SocketThread#{len(self.threads)}')
                logging.info('New client connected!')
                self.threads.append(new_user_thread)
                new_user_thread.start()
            except OSError: # On closing, socket will be deleted, thus socket.accept won't work!
                pass

    def handle_login(self, conn: socket.socket):
        magic_sentence = conn.recv(1024)
        if magic_sentence.decode() != 'WeAreSpyder':
            # Against crawlers & such: #savesomememory
            logging.warning('A client did not know the magic sentence!')
            conn.send(b'Connection not permitted!')
            conn.close()
            
        public_key, private_key = asymmetric.generate_keys()
        conn.send(public_key.to_bytes()) # Send public key

        fernet_key_encoded = conn.recv(1024) # Receive symmetric key
        fernet_key = symmetric.convert(asymmetric.decrypt(fernet_key_encoded, private_key))

        memory.erase_variable(fernet_key_encoded)

        conn.send(symmetric.encrypt(rndi.encrypt('UnitedWeStand').encode(), fernet_key)) # Send magic answer
        logging.info('Client verified!')


    def kill_threads(self):
        while True:
            if len(self.threads) == 0:
                break

            thread = self.threads[0]
            thread.kill()
            del self.threads[0]

    def cleanup(self):
        logging.info('Running cleanup...')
        self.run = False
        self.kill_threads()
        if self.fileno != -1: # Close socket if not closed
            self.close()
        atexit.unregister(self.cleanup)
        logging.info('Cleanup done!')