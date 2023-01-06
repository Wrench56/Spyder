from typing import Optional
from dataclasses import dataclass


@dataclass
class LoginData():
    username: Optional[str] = None
    password: Optional[str] = None
