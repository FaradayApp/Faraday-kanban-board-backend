from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Union


@dataclass
class CreateTaskEntry:
    title: str
    expiration_date: Union[date, str]
    performers: List[int]
    status: Optional[int]
    priority: Optional[int]
    description: str = ''
