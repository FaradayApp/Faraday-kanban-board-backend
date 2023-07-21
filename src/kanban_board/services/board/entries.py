from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CreateKanbanBoardEntry:
    group_id: str = None
