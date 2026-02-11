import os
import sys
from urllib.parse import urlparse

import pymysql
from yoyo import get_backend, read_migrations

def ensure_database_exists(db_uri: str) -> str:
    parsed = urlparse(db_uri)
    if parsed.scheme != 'mysql':
        return db_uri

    dbname = (parsed.path or '/').lstrip('/') or None
    if not dbname:
        return db_uri

    host = parsed.hostname or '127.0.0.1'
    port = parsed.port or 3306
    user = parsed.username or 'root'
    password = parsed.password or ''

    conn = pymysql.connect(host=host, port=port, user=user, password=password, charset='utf8mb4', autocommit=True)
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS `{}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(dbname))
    finally:
        conn.close()
    return db_uri


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/migrate.py <DB_URI> <MIGRATIONS_DIR>")
        sys.exit(1)

    db_uri = sys.argv[1]
    migrations_dir = sys.argv[2]

    db_uri = ensure_database_exists(db_uri)

    backend = get_backend(db_uri)
    migrations = read_migrations(migrations_dir)

    with backend.lock():
        pending = backend.to_apply(migrations)
        if not pending:
            print("No migrations to apply.")
            return
        backend.apply_migrations(pending)
        print(f"Applied {len(pending)} migration(s).")


if __name__ == '__main__':
    main()
