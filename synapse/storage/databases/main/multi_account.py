from typing import TYPE_CHECKING, List
import logging
import uuid

from synapse.storage._base import SQLBaseStore
from synapse.storage.database import (
    DatabasePool,
    LoggingDatabaseConnection,
    LoggingTransaction
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
    
    async def get_multi_account(self, user_id: str) -> int:
        row = await self.db_pool.simple_select_one(
            table="multi_account_user_association",
            keyvalues={"user_id ": user_id},
            retcols=(
                "multi_account_id",
            ),
            allow_none=True,
            desc="get_multi_account_id",
        )
        return row['user_id']

    async def create_multi_account(self, user_id: str) -> None:
        multi_account_id = await self.generate_uuid()

        await self.db_pool.simple_insert(
            "multi_accounts",
            {
                "id": multi_account_id
            },
            desc="insert_multi_account",
        )

        await self.db_pool.simple_insert(
            "multi_account_user_association",
            {
                "multi_account_id": multi_account_id,
                "user_id": user_id
            },
            desc="insert_multi_account",
        )

    async def get_multi_account_info(self, id: str) -> List[int]:
        row = await self.db_pool.simple_select_list(
            table="multi_account_user_association",
            keyvalues={"multi_account_id ": id},
            retcols=(
                "user_id ",
            ),
            allow_none=True,
            desc="get_users_in_multi_account",
        )
        return [entry["id"] for entry in row]

    async def add_user_to_multi_account(self, id: str, user_id: str) -> None:
        await self.db_pool.simple_insert(
            "multi_account_user_association",
            {
                "multi_account_id": id,
                "user_id": user_id
            },
            desc="insert_multi_account",
        )

    async def remove_user_from_multi_account(self, user_id: str) -> None:
        await self.db_pool.simple_delete_one(
            "multi_account_user_association",
            keyvalues={"user_id": user_id},
            desc="delete_user_from_multi_account",
        )


    async def delete_multi_account(self, id: str) -> None:
        await self.db_pool.simple_delete_many(
            "multi_account_user_association",
            keyvalues={"multi_account_id": id},
            desc="delete_users_from_multi_account",
        )

        await self.db_pool.simple_delete_one(
            "multi_accounts",
            keyvalues={"id": id},
            desc="delete_multi_account",
        )

    async def generate_uuid() -> str:
        return str(uuid.uuid4())
