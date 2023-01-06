from typing import Union

from cryptography.fernet import Fernet


def generate() -> bytes:
    return Fernet.generate_key()


def convert(key: Union[str, bytes]) -> Fernet:
    return Fernet(key)


def encrypt(string: bytes, key: Fernet) -> bytes:
    return key.encrypt(string)


def decrypt(string: Union[str, bytes], key: Fernet) -> bytes:
    return key.decrypt(string)
