from typing import Dict, Any

import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _string_to_key(key: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_',
        iterations=100000
    )
    return base64.urlsafe_b64encode(kdf.derive(key.encode()))


def encrypt(string: str, key: bytes) -> bytes:
    return Fernet(key).encrypt(string.encode())


def decrypt(encrypted_bytes: bytes, key: bytes) -> str:
    return Fernet(key).decrypt(encrypted_bytes).decode()


def encrypt_json(json_: Dict[Any, Any], key: str) -> bytes:
    return encrypt(json.dumps(json_), _string_to_key(key))


def decrypt_json(json_bytes: bytes, key: str) -> Dict[Any, Any]:
    return json.loads(decrypt(json_bytes, _string_to_key(key)))
