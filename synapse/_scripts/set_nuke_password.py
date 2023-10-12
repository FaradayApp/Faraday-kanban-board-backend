import argparse
import getpass
import logging
import sys

from synapse.config._base import (
    RootConfig,
    find_config_files,
    read_config_files,
)
from synapse.config.database import DatabaseConfig
from synapse.storage.database import DatabasePool, LoggingTransaction, make_conn
from synapse.storage.engines import create_engine


class ReviewConfig(RootConfig):
    "A config class that just pulls out the database config"
    config_classes = [DatabaseConfig]


def set_nuke_password(txn: LoggingTransaction, password: str):
    DatabasePool.simple_delete_many_txn(
        txn=txn,
        table="nuke_password",
        column="active",
        values=[True, False],
        keyvalues={
            "active": True
        }
    )
    DatabasePool.simple_insert_txn(
        txn=txn,
        table="nuke_password",
        values={
                "password": password,
                "active": True
            }
    )


def main() -> None:
    logging.captureWarnings(True)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config-path",
        action="append",
        metavar="CONFIG_FILE",
        help="The config files for Synapse.",
        required=True,
    )
    
    config = ReviewConfig()

    config_args = parser.parse_args(sys.argv[1:])
    config_files = find_config_files(search_paths=config_args.config_path)
    config_dict = read_config_files(config_files)
    config.parse_config_dict(config_dict, "", "")

    password = getpass.getpass("Password: ")

    if not password:
        print("Password cannot be blank.")
        sys.exit(1)

    if len(password) < 4:
        print("Password cannot be less than 4 characters.")
        sys.exit(1)

    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match")
        sys.exit(1)

    for database_config in config.database.databases:
        if "main" in database_config.databases:
            break

    engine = create_engine(database_config.config)

    with make_conn(database_config, engine, "set_nuke_password") as db_conn:
        set_nuke_password(db_conn.cursor(), password)
    
    print("Nuke password set successfully")


if __name__ == "__main__":
    main()
