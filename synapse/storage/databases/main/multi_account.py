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
        """Создать запись мультиаккаунта с двумя пользователями."""
        # Предположим, что у вас есть таблица multi_account_relations
        # с колонками user_id_1, user_id_2, user_id_3, user_id_4, user_id_5.
        # Давайте создадим запись с двумя пользователями user1_id и user2_id.

        # Определите SQL-запрос для вставки записи.
        sql = """
            INSERT INTO multi_account_relations (user_id_1, user_id_2)
            VALUES (?, ?)
        """

        # Выполните запрос, передав параметры.
        with self.db_pool.transaction() as txn:
            txn.execute(sql, (user1_id, user2_id))

    def get_multi_account_info(self, user_id: str) -> List[str]:
        """Получить информацию о мультиаккаунте (соединенных пользователях)
        из базы данных по пользователю переданному в метод."""
        # Предположим, что мультиаккаунты организованы так, что все связанные
        # пользователи перечислены в одной строке.
        # Например, "user_id_1", "user_id_2", и т.д.

        # Определите SQL-запрос для выбора соединенных пользователей.
        sql = """
            SELECT user_id_1, user_id_2, user_id_3, user_id_4, user_id_5
            FROM multi_account_relations
            WHERE user_id_1 = ? OR user_id_2 = ? OR user_id_3 = ? OR user_id_4 = ? OR user_id_5 = ?
        """

        # Выполните запрос, передав параметр user_id.
        with self.db_pool.transaction() as txn:
            txn.execute(sql, (user_id, user_id, user_id, user_id, user_id))
            rows = txn.fetchall()

        # Преобразуйте результат запроса в список соединенных пользователей.
        connected_users = []
        for row in rows:
            connected_users.extend(filter(None, row))  # Фильтруем None

        return connected_users

    def add_user_to_multi_account(self, user1_id: str, user2_id: str):
        """Добавить нового пользователя в мультиаккаунт."""
        # Для добавления пользователя в мультиаккаунт, найдите соответствующую запись
        # и добавьте нового пользователя в нее.

        # Определите SQL-запрос для обновления записи мультиаккаунта.
        sql = """
            UPDATE multi_account_relations
            SET user_id_3 = ?
            WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_2 = ? AND user_id_1 = ?)
        """

        # Выполните запрос, передав параметры.
        with self.db_pool.transaction() as txn:
            txn.execute(sql, (user2_id, user1_id, user2_id, user1_id, user2_id))

    def remove_user_from_multi_account(self, user1_id: str, user2_id: str):
        """Удалить пользователя из мультиаккаунта."""
        # Для удаления пользователя из мультиаккаунта, найдите соответствующую запись
        # и удалите пользователя из нее.

        # Определите SQL-запрос для обновления записи мультиаккаунта.
        sql = """
            UPDATE multi_account_relations
            SET user_id_3 = NULL
            WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_2 = ? AND user_id_1 = ?)
        """

        # Выполните запрос, передав параметры.
        with self.db_pool.transaction() as txn:
            txn.execute(sql, (user1_id, user2_id, user2_id, user1_id))

    def delete_multi_account(self, user1_id: str):
        """Удалить мультиаккаунт."""
        # Для удаления мультиаккаунта найдите соответствующую запись и удалите ее.

        # Определите SQL-запрос для удаления записи мультиаккаунта.
        sql = """
            DELETE FROM multi_account_relations
            WHERE user_id_1 = ? OR user_id_2 = ?
        """

        # Выполните запрос, передав параметры.
        with self.db_pool.transaction() as txn:
            txn.execute(sql, (user1_id, user1_id))
