import synapse.config.homeserver
import synapse.storage.engines
import synapse.storage.types


def run_create(
    cur: synapse.storage.types.Cursor,
    database_engine: synapse.storage.engines.BaseDatabaseEngine,
) -> None:
    if isinstance(database_engine, synapse.storage.engines.PostgresEngine):
        select_sql = """
            CREATE TABLE IF NOT EXISTS multi_accounts (
                id TEXT PRIMARY KEY
            );

            CREATE TABLE IF NOT EXISTS multi_account_user_association (
                multi_account_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY (multi_account_id) REFERENCES multi_accounts(id)
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
            CREATE TABLE IF NOT EXISTS multi_accounts (
                id TEXT PRIMARY KEY
            );

            CREATE TABLE IF NOT EXISTS multi_account_user_association (
                multi_account_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY (multi_account_id) REFERENCES multi_accounts(id)
            );
        """
        cur.execute(select_sql)
