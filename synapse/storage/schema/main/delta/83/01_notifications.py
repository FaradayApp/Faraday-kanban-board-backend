import synapse.config.homeserver
import synapse.storage.engines
import synapse.storage.types


def run_create(
    cur: synapse.storage.types.Cursor,
    database_engine: synapse.storage.engines.BaseDatabaseEngine,
) -> None:
    if isinstance(database_engine, synapse.storage.engines.PostgresEngine):
        select_sql = """
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                text TEXT NOT NULL,
                date DATE
            );

            CREATE TABLE IF NOT EXISTS notifications_viewed_by_user_association (
                notification_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY (notification_id) REFERENCES notifications(id)
            );
        """
        cur.execute(select_sql)

def run_upgrade(
    cur: synapse.storage.types.Cursor,
    database_engine: synapse.storage.engines.BaseDatabaseEngine,
    config: synapse.config.homeserver.HomeServerConfig,
) -> None:
    if isinstance(database_engine, synapse.storage.engines.PostgresEngine):
        select_sql = """
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                text TEXT NOT NULL,
                date DATE
            );

            CREATE TABLE IF NOT EXISTS notifications_viewed_by_user_association (
                notification_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY (notification_id) REFERENCES notifications(id)
            );
        """
        cur.execute(select_sql)
