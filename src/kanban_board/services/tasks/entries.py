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


@dataclass
class EditTaskEntry:
    title: Optional[str] = None
    expiration_date: Optional[Union[date, str]] = None
    performers: Optional[List[int]] = None
    status: Optional[int] = None
    priority: Optional[int] = None
    description: Optional[str] = None
