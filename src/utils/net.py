import requests
import socket

def connection():
    try:
        requests.get('https://google.com', timeout=1.0)
        return True
    except requests.exceptions.ConnectTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False

def get_local_ip():
    return socket.gethostbyname(str(socket.gethostname()))