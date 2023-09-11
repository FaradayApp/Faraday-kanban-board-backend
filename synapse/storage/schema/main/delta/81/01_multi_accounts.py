import synapse.config.homeserver
import synapse.storage.engines
import synapse.storage.types


def run_create(
    cur: synapse.storage.types.Cursor,
    database_engine: synapse.storage.engines.BaseDatabaseEngine,
) -> None:
    if isinstance(database_engine, synapse.storage.engines.PostgresEngine):
        select_sql = """
            CREATE TABLE IF NOT EXISTS multi_account_relations (
            user_id_1 TEXT,
            user_id_2 TEXT,
            user_id_3 TEXT,
            user_id_4 TEXT,
            user_id_5 TEXT,
            PRIMARY KEY (user_id_1, user_id_2, user_id_3, user_id_4, user_id_5)
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
            CREATE TABLE IF NOT EXISTS multi_account_relations (
            user_id_1 TEXT,
            user_id_2 TEXT,
            user_id_3 TEXT,
            user_id_4 TEXT,
            user_id_5 TEXT,
            PRIMARY KEY (user_id_1, user_id_2, user_id_3, user_id_4, user_id_5)
            );
        """
        cur.execute(select_sql)
