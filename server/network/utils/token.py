import binascii
import os

def generate():
    # Generate 32 bytes long random token!
    return binascii.hexlify(os.urandom(16)).decode()