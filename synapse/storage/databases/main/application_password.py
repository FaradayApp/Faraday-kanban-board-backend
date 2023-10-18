from typing import TYPE_CHECKING, List
import logging
import uuid

from synapse.storage._base import SQLBaseStore
from synapse.storage.database import (
    DatabasePool,
    LoggingDatabaseConnection
)

if TYPE_CHECKING:
    from synapse.server import HomeServer


logger = logging.getLogger(__name__)

class ApplicationPasswordStore(SQLBaseStore):
    def __init__(
        self,
        database: DatabasePool,
        db_conn: LoggingDatabaseConnection,
        hs: "HomeServer",
    ):
        super().__init__(database, db_conn, hs)
    
    async def get_application_password(self, user_id: str) -> int:
        return await self.db_pool.simple_select_one(
            table="application_password",
            keyvalues={"user_id ": user_id},
            retcols=(
                "password",
            ),
            allow_none=True,
            desc="get_application_password",
        )

    async def create_application_password(self, user_id: str, password: str) -> None:
        await self.db_pool.simple_insert(
            "application_password",
            {
                "user_id": user_id,
                "password": password
            },
            desc="insert_application_password",
        )

    async def delete_application_password(self, user_id: str) -> None:
        await self.db_pool.simple_delete_one(
            "application_password",
            keyvalues={"user_id": user_id},
            desc="delete_application_password",
        )
