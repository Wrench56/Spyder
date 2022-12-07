from encryption import symmetric, rndinjection as rndi

# Wrapper for easier encrypted message sending!
def send(struct, message):
    struct.socket.send(symmetric.encrypt(rndi.encrypt(message).encode(), struct.fernet_key))