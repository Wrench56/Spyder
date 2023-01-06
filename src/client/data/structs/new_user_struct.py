from typing import Optional
from dataclasses import dataclass


@dataclass
class NewUserData():
    username: Optional[str] = None
    password: Optional[str] = None
