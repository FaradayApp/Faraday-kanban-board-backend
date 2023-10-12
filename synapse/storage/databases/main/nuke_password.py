from typing import TYPE_CHECKING
import logging

from synapse.storage._base import SQLBaseStore
from synapse.storage.database import (
    DatabasePool,
    LoggingDatabaseConnection
)

if TYPE_CHECKING:
    from synapse.server import HomeServer


logger = logging.getLogger(__name__)

class NukePasswordStore(SQLBaseStore):
    def __init__(
        self,
        database: DatabasePool,
        db_conn: LoggingDatabaseConnection,
        hs: "HomeServer",
    ):
        super().__init__(database, db_conn, hs)
    
    async def get_actual_nuke_password(self) -> int:
        return await self.db_pool.simple_select_one(
            table="nuke_password",
            keyvalues={"active ": True},
            retcols=(
                "password",
            ),
            allow_none=True,
            desc="get_actual_nuke_password",
        )
