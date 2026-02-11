import os
import sys
import argparse
from urllib.parse import urlparse
import pymysql
import shutil
from yoyo import get_backend, read_migrations

from app.config import env_db_uri, FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from dotenv import load_dotenv


DEFAULT_MIGRATIONS_DIR = "migrations"

def ensure_database_exists(db_uri: str) -> None:
    """Pastikan database MySQL ada — jika belum, buat otomatis."""
    parsed = urlparse(db_uri)
    if parsed.scheme != "mysql":
        print("❌ Hanya mendukung MySQL.")
        return

    dbname = (parsed.path or "/").lstrip("/") or None
    if not dbname:
        print("❌ Nama database tidak ditemukan di URI.")
        return

    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 3306
    user = parsed.username or "root"
    password = parsed.password or ""

    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="utf8mb4",
            autocommit=True,
        )
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbname}` "
                f"DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        print(f"✅ Database `{dbname}` siap digunakan.")
    except Exception as e:
        print(f"❌ Gagal memastikan database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


def cmd_migrate(db_uri: str, migrations_dir: str) -> int:
    ensure_database_exists(db_uri)
    backend = get_backend(db_uri)
    migrations = read_migrations(migrations_dir)

    with backend.lock():
        pending = backend.to_apply(migrations)
        if not pending:
            print("✅ Tidak ada migration yang perlu dijalankan.")
            return 0

        backend.apply_migrations(pending)
        print(f"✅ {len(pending)} migration berhasil dijalankan.")
        return 0


def cmd_serve() -> int:
    load_dotenv()
    from app.main import create_app

    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
    return 0


def cmd_cache_clear() -> int:
    """Hapus semua __pycache__ dan file .pyc."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    removed_dirs = 0
    removed_files = 0

    for current_dir, dirnames, filenames in os.walk(project_root):
        if "__pycache__" in dirnames:
            cache_dir = os.path.join(current_dir, "__pycache__")
            try:
                shutil.rmtree(cache_dir, ignore_errors=True)
                removed_dirs += 1
            except Exception:
                pass

        for fname in list(filenames):
            if fname.endswith(".pyc"):
                fpath = os.path.join(current_dir, fname)
                try:
                    os.remove(fpath)
                    removed_files += 1
                except Exception:
                    pass

    print(f"🧹 Cleared {removed_dirs} __pycache__ folder(s) and {removed_files} .pyc file(s).")
    return 0


def main() -> int:
    """CLI runner utama proyek."""
    load_dotenv()

    parser = argparse.ArgumentParser(prog="run.py", description="Project runner CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("migrate", help="Auto-create DB dan apply yoyo migrations")
    sub.add_parser("serve", help="Jalankan Flask development server")
    sub.add_parser("cache:clear", help="Hapus semua __pycache__ dan .pyc")

    args = parser.parse_args()

    if args.command == "migrate":
        db_uri = env_db_uri()
        migrations_dir = os.getenv("MIGRATIONS_DIR", DEFAULT_MIGRATIONS_DIR)
        return cmd_migrate(db_uri, migrations_dir)

    elif args.command == "serve":
        return cmd_serve()

    elif args.command == "cache:clear":
        return cmd_cache_clear()

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
