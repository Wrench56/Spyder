from dataclasses import dataclass, field

@dataclass
class ClientData():
    socket: object|None = None
    fernet_key: object = None

    username: str = ''
    hash_: str = ''
    
    is_user: bool|None = None
    is_server: bool|None = None
    is_invite: bool|None = None
    is_link: bool|None = None
    is_authenticated: bool|None = None

    new_json: dict = field(default_factory=dict)

