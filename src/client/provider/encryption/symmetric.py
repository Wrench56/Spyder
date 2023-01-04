from cryptography.fernet import Fernet


def generate():
    return Fernet.generate_key()


def convert(key):
    return Fernet(key)


def encrypt(string: bytes, key):
    return key.encrypt(string)


def decrypt(string: bytes, key):
    return key.decrypt(string)
