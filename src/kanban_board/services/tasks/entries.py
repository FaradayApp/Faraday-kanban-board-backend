from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class CreateTaskEntry:
    board: int
    title: str
    description: str = ''
    expiration_date: date
    performer: List[int]
    status: Optional[int]
    priority: Optional[int]
