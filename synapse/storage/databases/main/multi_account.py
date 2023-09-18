from typing import TYPE_CHECKING, List
import logging

from synapse.storage._base import SQLBaseStore
from synapse.storage.database import (
    DatabasePool,
    LoggingDatabaseConnection
)

if TYPE_CHECKING:
    from synapse.server import HomeServer


logger = logging.getLogger(__name__)

class MultiAccountStore(SQLBaseStore):
    def __init__(
        self,
        database: DatabasePool,
        db_conn: LoggingDatabaseConnection,
        hs: "HomeServer",
    ):
        super().__init__(database, db_conn, hs)

    def create_multi_account(self, user1_id: str, user2_id: str):
        pass

    def get_multi_account_info(self, user_id: str) -> List[str]:
        pass

    def add_user_to_multi_account(self, user1_id: str, user2_id: str):
        pass

    def remove_user_from_multi_account(self, user1_id: str, user2_id: str):
        pass

    def delete_multi_account(self, user1_id: str):
        pass
