from pathlib import Path
from importlib import import_module

from . import key_manager


def run_migrations(conn):
    migrations_dir = Path(__file__).with_name("migrations")
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    for path in sorted(migrations_dir.glob("*.py")):
        if path.name.startswith("__"):
            continue
        version = int(path.stem.split("_")[0])
        if version > current:
            module = import_module(f"{__name__}.migrations.{path.stem}")
            module.upgrade(conn)
            conn.execute(f"PRAGMA user_version = {version}")


from .encrypted_store import SaveManager


__all__ = ["SaveManager", "key_manager", "run_migrations"]
