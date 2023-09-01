from typing import List, Dict, Callable, Any

import os
import logging
import shutil
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from utils.art import LOGIN_FILE_WARNING


class StepFailed(Exception):
    def __init__(self, step: int, *args: List[Any]) -> None:
        self.step: int = step
        super().__init__(*args)


# PARTIALLY WRITTEN BY CHAT GPT - 11.12.2022 - (WANTED TO TEST IT)
def _encrypt_json(json_: Dict[Any, Any], key: str) -> bytes:
    password = key.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    fernet_key = base64.urlsafe_b64encode(kdf.derive(password))
    fernet = Fernet(fernet_key)

    json_bytes = str(json_).encode()
    encrypted_json = fernet.encrypt(json_bytes)

    return encrypted_json


def run_all(status_func: Callable[[str, str], None], new_user_struct: object) -> None:
    prev_cwd = os.getcwd()
    src = os.path.realpath(__file__).replace('\\utils\\create_user.py', '').replace('/utils/create_user.py', '')
    os.chdir(f'{src}/data/users/')
    try:
        _create_user_folder(status_func, new_user_struct.username)
        config_key = _create_user_config(status_func, new_user_struct.username)
        _create_logins_file(status_func, new_user_struct.username, new_user_struct.password, config_key)
        status_func('USER READY TO USE', ' OK ')
    except StepFailed as error:
        if error.step > 0:
            logging.critical(f'Deleting progress in {new_user_struct.username} folder!')
            shutil.rmtree(f'{os.getcwd()}/{new_user_struct.username}/')
    finally:
        os.chdir(prev_cwd)


def _create_user_folder(status_func: Callable[[str, str], None], username: str) -> None:
    if os.path.exists(f'{os.getcwd()}/{username}'):
        logging.critical('User already exists!')
        status_func('User directory created', 'FAIL')
        raise StepFailed(0)

    os.mkdir(f'{os.getcwd()}/{username}')
    status_func('User directory created', ' OK ')


def _create_user_config(status_func: Callable[[str, str], None], username: str) -> bytes:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    os.mkdir(f'./{username}/config')
    with open(f'./{username}/config/config.yaml', 'wb') as cfile:
        cfile.write(fernet.encrypt(b'Hello World'))
        cfile.close()
    status_func('Config files created', ' OK ')

    return key


def _create_logins_file(status_func: Callable[[str, str], None], username: str, password: str, config_key: bytes) -> None:
    os.mkdir(f'./{username}/secrets')
    json_ = {
        'VERSION': 1.0,
        'USERNAME': username,
        'CONFIG_PASSWORD': config_key,
        'LAST_SEEN': ''
    }

    with open(f'./{username}/secrets/login.conf', 'wb') as lfile:
        lfile.write(LOGIN_FILE_WARNING.encode())
        lfile.write(_encrypt_json(json_, password))
        lfile.close()

    status_func('Login file created', ' OK ')
