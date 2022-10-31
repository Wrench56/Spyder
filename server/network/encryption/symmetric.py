from cryptography.fernet import Fernet

def generate():
    return Fernet.generate_key()

def convert(key):
    return Fernet(key)

def encrypt(string: str, key):
    return key.encrypt(string.encode())

def decrypt(string: str, key):
    return key.decode(string)
