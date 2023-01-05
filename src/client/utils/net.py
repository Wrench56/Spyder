import socket

import requests


def connection() -> bool:
    try:
        requests.get('https://google.com', timeout=5.0)
        return True
    except requests.exceptions.ConnectTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False


def get_local_ip() -> str:
    return socket.gethostbyname(socket.gethostname())
