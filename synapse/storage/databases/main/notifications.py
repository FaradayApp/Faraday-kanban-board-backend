import datetime
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

class NotificationsStore(SQLBaseStore):
    def __init__(
        self,
        database: DatabasePool,
        db_conn: LoggingDatabaseConnection,
        hs: "HomeServer",
    ):
        super().__init__(database, db_conn, hs)
    
    async def get_all_notifications(self, user_id: str) -> int:
        raw = await self.db_pool.simple_select_list(
            table="notifications",
            keyvalues={},
            retcols=(
                "id ",
                "user_id",
                "text",
                "date"
            ),
            desc="get_all_notifications",
        )
        return await self.add_viewed_in_raw(raw=raw, user_id=user_id)
    
    async def add_viewed_in_raw(self, raw: List, user_id: str):
        result = []
        for entry in raw:
            viewed = await self.db_pool.simple_select_one(
                table="notifications_viewed_by_user_association",
                keyvalues={
                    "user_id ": user_id,
                    "notification_id": entry['id']
                },
                retcols=(
                    "notification_id",
                ),
                allow_none=True,
                desc="get_viewed_user",
            )
            if viewed["notification_id"]: 
                entry["viewed"] = True
            else:
                entry["viewed"] = False
            result.append(entry)
        return result

    async def create_notification(self, user_id: str, text: str) -> None:
        await self.db_pool.simple_insert(
            "notifications",
            {
                "id ": await self.generate_uuid(),
                "user_id": user_id,
                "text": text,
                "date": await datetime.date.today().strftime('%Y-%m-%d')
            },
            desc="insert_new_notification",
        )
    
    async def add_user_to_viewed(self, user_id: str, notification_id: str):
        await self.db_pool.simple_insert(
            "notifications_viewed_by_user_association",
            {
                "notification_id": notification_id,
                "user_id": user_id
            },
            desc="insert_viewed_user",
        )

    async def generate_uuid(self) -> str:
        return str(uuid.uuid4())
