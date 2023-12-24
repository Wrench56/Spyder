from typing import List, Callable, Any

import os
import logging
import shutil

from cryptography.fernet import Fernet

from utils import art, constants, encryption


class StepFailed(Exception):
    def __init__(self, step: int, *args: List[Any]) -> None:
        self.step: int = step
        super().__init__(*args)


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
        logging.info(f'User directory "{new_user_struct.username}" created successfully!')


def _create_user_folder(status_func: Callable[[str, str], None], username: str) -> None:
    if os.path.exists(f'./{username}'):
        logging.critical('User already exists!')
        status_func('User directory created', 'FAIL')
        raise StepFailed(0)

    os.mkdir(f'./{username}')
    os.mkdir(f'./{username}/secrets')
    status_func('User directory created', ' OK ')


def _create_user_config(status_func: Callable[[str, str], None], username: str) -> bytes:
    key = Fernet.generate_key()
    with open(f'./{username}/secrets/config.bin', 'wb') as cfile:
        cfile.write(encryption.encrypt_json({'username': username}, key))
        cfile.close()
    status_func('Config files created', ' OK ')

    return key


def _create_logins_file(status_func: Callable[[str, str], None], username: str, password: str, config_key: bytes) -> None:
    json_ = {
        'VERSION': constants.VERSION,
        'USERNAME': username,
        'CONFIG_PASSWORD': config_key.decode(),  # fernet.generate_key() is already base64 (urlsafe) encoded
        'LAST_SEEN': ''
    }

    with open(f'./{username}/secrets/login.bin', 'wb') as lfile:
        lfile.write(art.LOGIN_FILE_WARNING.encode())
        lfile.write(encryption.encrypt_json(json_, encryption.s2k(password)))
        lfile.close()

    status_func('Login file created', ' OK ')
