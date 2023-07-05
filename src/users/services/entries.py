from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntry:
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
