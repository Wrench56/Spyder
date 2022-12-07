import socket
import atexit
import logging
import json

from encryption import symmetric, asymmetric, rndinjection as rndi
from utils import memory, threads
from utils.operations import handler, login
from data.structs import client_struct

class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.threads = []
        self.run = True

        atexit.register(self.cleanup)

    def start(self, ip, port):
        try:
            self.bind((ip, port))
        except OSError as e:
            if e.args[0] == 10048: # Port already in use!
                logging.critical('The specified port for the server is already in use!')
                exit()

        

        accept_new_thread = threads.DestroyableThread(target=self.accept_new)
        accept_new_thread.setName('AcceptNewUserThread')
        self.threads.append(accept_new_thread)
        accept_new_thread.start()
    
    def accept_new(self):
        while self.run:
            self.listen()
            try:
                conn, _ = self.accept()
                new_user_thread = threads.SocketThread(target=self.handle_login, args=(conn, len(self.threads)))
                new_user_thread.setName(f'SocketThread#{len(self.threads)}')
                logging.info(f'New client connected! Active clients: {len(self.threads)}')
                self.threads.append(new_user_thread)
                new_user_thread.start()
            except OSError: # On closing, socket will be deleted, thus socket.accept won't work!
                pass

    def handle_login(self, conn: socket.socket, thread_number: int):
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
        logging.debug('Client verified!')

        self.handle_operations(conn, fernet_key)

        # Kill thread & GC
        self.threads[thread_number].kill()
        del self.threads[thread_number]


    def handle_operations(self, conn: socket.socket, fernet_key):
        client_data = client_struct.ClientData()
        client_data.socket = conn
        client_data.fernet_key = fernet_key

        while True:
            try:
                message_encoded = conn.recv(1024)
            except ConnectionResetError:
                logging.warn('Client closed connection unexpectedly!')
                break

            if message_encoded == b'': # Disconnected!
                logging.warn('Client closed connection unexpectedly!')
                break

            message = rndi.decrypt(symmetric.decrypt(message_encoded, fernet_key).decode())
            logging.debug(f'New operation received: {message}')
            try:
                op_json = json.loads(message)
            except json.decoder.JSONDecodeError:
                logging.error('Client sent invalid operation format!')
            
            client_data.new_json = op_json
            handler.handle_operation(client_data)
        return

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