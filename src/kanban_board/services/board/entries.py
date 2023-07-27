from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CreateKanbanBoardEntry:
    title: str = None
