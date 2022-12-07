from typing import ByteString
import rsa

# Simple wrapper module for rsa
# Later on I MIGHT change to pycryptodome because of effectiveness (as it uses C modules as well)

class Key:
    def __init__(self, key = None) -> None:
        if key is not None:
            self.key = key

    def to_bytes(self) -> ByteString:
        return self.key.save_pkcs1(format='DER')
    
    def from_bytes(self, bkey) -> None:
        self.key = rsa.PublicKey.load_pkcs1(bkey, format='DER')
    
def generate_keys():
    public_key, private_key = rsa.newkeys(1024)
    return Key(public_key), Key(private_key)

def encrypt(string: bytes, key: Key) -> bytes:
    return rsa.encrypt(string, key.key)

def decrypt(string: bytes, key: Key) -> bytes:
    return rsa.decrypt(string, key.key)