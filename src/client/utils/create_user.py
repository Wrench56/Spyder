import os
import logging
import shutil
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class StepFailed(Exception):
    def __init__(self, step, *args) -> None:
        self.step = step
        super().__init__(*args)


# PARTIALLY WRITTEN BY CHAT GPT - 11.12.2022 - (WANTED TO TEST IT)
def _encrypt_json(json_: dict, key: str):
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

    return encrypted_json.decode()


def run_all(status_func, new_user_struct):
    prev_cwd = os.getcwd()
    src = os.path.realpath(__file__).replace("\\utils\\create_user.py", "").replace("/utils/create_user.py", "")
    os.chdir(f'{src}/data/users/')
    try:
        _create_user_folder(status_func, new_user_struct.username)
        _create_user_config(status_func, new_user_struct.username)
        _create_logins_file(status_func, new_user_struct.username, new_user_struct.password)
        status_func('USER READY TO USE', ' OK ')
    except StepFailed as e:
        if e.step > 0:
            logging.critical(f'Deleting progress in {new_user_struct.username} folder!')
            shutil.rmtree(f'{os.getcwd()}/{new_user_struct.username}/')
    finally:
        os.chdir(prev_cwd)


def _create_user_folder(status_func, username):
    if os.path.exists(f'{os.getcwd()}/{username}'):
        logging.critical('User already exists!')
        status_func('User directory created', 'FAIL')
        raise StepFailed(0)

    os.mkdir(f'{os.getcwd()}/{username}')
    status_func('User directory created', ' OK ')


def _create_user_config(status_func, username):
    os.mkdir(f'./{username}/config')
    with open(f'./{username}/config/config.yaml', 'w') as cfile:
        cfile.close()
    status_func('Config files created', ' OK ')


def _create_logins_file(status_func, username, password):
    os.mkdir(f'./{username}/secrets')
    json_ = {'VERSION': 1.0}
    write_ = f'''
    ////////// WARNING! //////////
    // MANAGED BY SPYDER CHAT!  //
    // DO NOT MODIFY ANYTHING   //
    // BY HAND OR ELSE THIS     //
    // CONFIG MIGHT BREAK.      //
    // IF YOU ARE NOT THE OWNER //
    // OF THIS USER GET OUT!    //
    //////////////////////////////

    {_encrypt_json(json_, password)}
    '''

    with open(f'./{username}/secrets/login.conf', 'w') as lfile:
        lfile.write(write_)
        lfile.close()

    status_func('Login file created', ' OK ')
