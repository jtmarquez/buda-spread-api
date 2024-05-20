from peewee import SqliteDatabase

from config.env_vars import DATABASE_NAME


database = SqliteDatabase(
    DATABASE_NAME,
    pragmas={
        "journal_mode": "wal",
        "cache_size": 10000,  # 10000 pages, or ~40MB
        "foreign_keys": 1,  # Enforce foreign-key constraints
    },
)
