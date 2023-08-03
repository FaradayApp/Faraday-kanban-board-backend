from dataclasses import dataclass
from io import BytesIO
from typing import Optional, Union


@dataclass
class UserEntry:
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Union[str, BytesIO] = None


@dataclass
class EditUserEntry:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Union[str, BytesIO] = None
